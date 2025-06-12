import os
import uuid
import pytesseract
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
import PyPDF2
from PIL import Image
import io
import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
import asyncio

app = FastAPI()

# Initialize OpenAI client
client = OpenAI(api_key="your-openai-api-key")

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chroma_db")
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="documents", embedding_function=embedding_function)

# Directory to store uploaded documents
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    query: str
    exclude_docs: List[str] = []

# Extract text from PDF
def extract_text_from_pdf(file_path: str) -> List[str]:
    text_per_page = []
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text() or ""
            text_per_page.append(text)
    return text_per_page

# Extract text from image using OCR
def extract_text_from_image(file_path: str) -> str:
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img)
    return text

# Split text into paragraphs
def split_into_paragraphs(text: str) -> List[str]:
    return [para.strip() for para in text.split("\n\n") if para.strip()]

# Store document in ChromaDB
def store_document(doc_id: str, file_path: str, filename: str):
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext == ".pdf":
        pages = extract_text_from_pdf(file_path)
    elif file_ext in [".png", ".jpg", ".jpeg"]:
        pages = [extract_text_from_image(file_path)]
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            pages = [f.read()]

    for page_num, text in enumerate(pages, 1):
        paragraphs = split_into_paragraphs(text)
        for para_num, paragraph in enumerate(paragraphs, 1):
            collection.add(
                documents=[paragraph],
                metadatas=[{"document_id": doc_id, "filename": filename, "page": page_num, "paragraph": para_num}],
                ids=[f"{doc_id}_p{page_num}_para{para_num}"]
            )

# Process a single file upload
def process_file(file: UploadFile, doc_id: str):
    file_ext = os.path.splitext(file.filename)[1].lower()
    file_path = os.path.join(UPLOAD_DIR, f"{doc_id}{file_ext}")
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    store_document(doc_id, file_path, file.filename)
    return {"doc_id": doc_id, "filename": file.filename}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    uploaded_files = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_file, file, str(uuid.uuid4())) for file in files]
        for future in futures:
            uploaded_files.append(future.result())
    return JSONResponse(content={"message": "Files uploaded successfully", "files": uploaded_files})

@app.get("/documents")
async def list_documents():
    unique_docs = set()
    for metadata in collection.get(include=["metadatas"])["metadatas"]:
        unique_docs.add((metadata["document_id"], metadata["filename"]))
    return JSONResponse(content={"documents": [{"doc_id": doc_id, "filename": filename} for doc_id, filename in unique_docs]})

async def search_document(query: str, doc_id: str):
    results = collection.query(query_texts=[query], n_results=2, where={"document_id": doc_id})
    answers = []
    for doc, metadata in zip(results["documents"][0], results["metadatas"][0]):
        answers.append({
            "document_id": metadata["document_id"],
            "filename": metadata["filename"],
            "extracted_answer": doc,
            "citation": f"Page {metadata['page']}, Para {metadata['paragraph']}"
        })
    return answers

@app.post("/query")
async def query_documents(request: QueryRequest):
    query = request.query
    exclude_docs = request.exclude_docs

    # Get all document IDs
    doc_ids = {m["document_id"] for m in collection.get(include=["metadatas"])["metadatas"]} - set(exclude_docs)

    # Parallel search across documents
    answers = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(asyncio.run, search_document(query, doc_id)) for doc_id in doc_ids]
        for future in futures:
            answers.extend(future.result())

    # Theme identification using OpenAI
    prompt = f"""
    Given the following query: "{query}"
    And the following document excerpts:
    {chr(10).join([f"- {ans['filename']}: {ans['extracted_answer']} ({ans['citation']})" for ans in answers])}
    
    Identify and summarize the main themes across these excerpts. For each theme, provide a brief summary and list the supporting documents with their citations.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    themes = response.choices[0].message.content.strip()

    return JSONResponse(content={"answers": answers, "themes": themes})
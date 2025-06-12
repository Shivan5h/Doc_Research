import streamlit as st
import httpx
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict
import asyncio

# Cache document list
@st.cache_data
def fetch_documents() -> List[Dict]:
    try:
        with httpx.Client() as client:
            response = client.get("http://localhost:8000/documents")
            response.raise_for_status()
            return response.json()["documents"]
    except httpx.RequestError:
        return []

# Cache query results
@st.cache_data
def fetch_query_results(query: str, exclude_docs: tuple) -> Dict:
    try:
        with httpx.Client() as client:
            response = client.post("http://localhost:8000/query", json={"query": query, "exclude_docs": list(exclude_docs)})
            response.raise_for_status()
            return response.json()
    except httpx.RequestError:
        return {"answers": [], "themes": ""}

st.title("Document Research & Theme Identification Chatbot")

# File upload with progress bar
uploaded_files = st.file_uploader("Upload Documents", type=["pdf", "png", "jpg", "jpeg", "txt"], accept_multiple_files=True)
if uploaded_files:
    st.write("Uploading files...")
    progress_bar = st.progress(0)
    async def upload_file(file):
        async with httpx.AsyncClient() as client:
            files = {"files": (file.name, file, file.type)}
            response = await client.post("http://localhost:8000/upload", files=files)
            return response.status_code == 200

    async def upload_all_files():
        tasks = [upload_file(file) for file in uploaded_files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    with ThreadPoolExecutor(max_workers=4) as executor:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(upload_all_files())
        loop.close()

    for i, success in enumerate(results):
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    if all(results):
        st.success("Files uploaded successfully!")
        st.cache_data.clear()  # Clear cache to refresh document list
    else:
        st.error("Error uploading some files.")

# Display uploaded documents
st.subheader("Uploaded Documents")
docs = fetch_documents()
if docs:
    st.dataframe(pd.DataFrame(docs, columns=["Document ID", "Filename"]))
else:
    st.write("No documents uploaded yet.")

# Query interface
st.subheader("Ask a Question")
query = st.text_input("Enter your question:")
exclude_docs = st.multiselect("Exclude Documents", options=[doc["doc_id"] for doc in docs], default=[])
if st.button("Submit Query"):
    if query:
        with st.spinner("Processing query..."):
            result = fetch_query_results(query, tuple(exclude_docs))
            
            # Display individual answers
            st.subheader("Individual Document Answers")
            answers = result["answers"]
            if answers:
                df = pd.DataFrame(answers, columns=["document_id", "filename", "extracted_answer", "citation"])
                df = df.rename(columns={"document_id": "Document ID", "filename": "Filename", "extracted_answer": "Extracted Answer", "citation": "Citation"})
                st.dataframe(df)
            else:
                st.write("No relevant answers found.")
            
            # Display themes
            st.subheader("Identified Themes")
            st.markdown(result["themes"])
    else:
        st.warning("Please enter a question.")
Document Research & Theme Identification Chatbot
A web-based chatbot that ingests 75+ documents (PDFs, images, text), answers user queries with precise paragraph-level citations, and identifies common themes across documents. Built with FastAPI, Streamlit, OpenAI, ChromaDB, and Tesseract OCR, optimized with parallel processing and caching for performance.
Table of Contents

Features
Tech Stack
Prerequisites
Installation
Running Locally
Deployment on Streamlit Community Cloud
Usage
Project Structure
Dataset
Performance Optimizations
Limitations
Future Improvements
Contributing
License

Features

Document Upload: Supports 75+ documents (PDFs, images [.png, .jpg, .jpeg], text) with OCR for scanned images.
Query Processing: Natural language queries with answers extracted from documents, including paragraph-level citations (e.g., "Page 4, Para 2").
Theme Identification: Summarizes common themes across document answers with supporting citations.
Web Interface: Streamlit UI for uploading files, viewing documents, querying, and excluding specific documents from searches.
Performance: Parallel processing for uploads and queries, caching for repeated operations, and async API calls.
Extra Features: Document exclusion, tabular answer display, and progress feedback for uploads.

Tech Stack

Backend: FastAPI (Python) for API endpoints.
Frontend: Streamlit for the web interface.
LLM: OpenAI GPT-4o-mini for theme identification.
Vector Search: ChromaDB with SentenceTransformer embeddings.
OCR: Tesseract for extracting text from images.
Dependencies: PyPDF2, Pillow, httpx, concurrent.futures.
Deployment: Streamlit Community Cloud (frontend), Render (backend).

Prerequisites

Python: 3.9+
Tesseract OCR: Installed and accessible in system PATH.
OpenAI API Key: Obtain from OpenAI.
Git: For version control.
Streamlit Community Cloud Account: Sign up at Streamlit Community Cloud.
Render Account: Sign up at Render for backend deployment.

Installation

Clone the Repository:
git clone https://github.com/Shivan5h/Doc-Research.git
cd Doc-Research


Install Tesseract OCR:

Ubuntu: sudo apt-get install tesseract-ocr
macOS: brew install tesseract
Windows: Download from Tesseract GitHub and add to PATH.


Install Python Dependencies:
pip install -r requirements.txt


Set Environment Variables:
export OPENAI_API_KEY='your-api-key'
export BACKEND_URL='http://localhost:8000'

On Windows, use set instead of export.


Running Locally

Start the FastAPI Backend:
uvicorn main:app --host 0.0.0.0 --port 8000


Start the Streamlit Frontend (in a new terminal):
streamlit run app.py


Access the App:

Open http://localhost:8501 in your browser for the Streamlit UI.
The backend runs on http://localhost:8000.



Deployment on Streamlit Community Cloud
Streamlit Community Cloud hosts the Streamlit frontend, but the FastAPI backend requires a separate service like Render due to Streamlit's limitations with non-Streamlit apps.
Deploy FastAPI Backend (on Render)

Push to GitHub:

Ensure your repository includes main.py, requirements.txt, and other necessary files.
Push to GitHub:git add .
git commit -m "Prepare for deployment"
git push origin main




Set Up Render:

Create a new web service on Render.
Select your GitHub repository.
Configure:
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT


Add environment variable: OPENAI_API_KEY=your-api-key.
Deploy and note the backend URL (e.g., https://your-backend.onrender.com).


Update app.py:

Modify app.py to use the Render backend URL and environment variables:import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
# Example API call
response = client.get(f"{BACKEND_URL}/documents")


Update all API calls in app.py to use BACKEND_URL.



Deploy Streamlit Frontend

Prepare for Streamlit Cloud:

Ensure app.py, requirements.txt, and other files are in the repository root.
Update app.py to use environment variables for the backend URL and OpenAI API key (already implemented in the optimized version).
Commit and push changes to GitHub:git add app.py
git commit -m "Update app.py for environment variables"
git push origin main




Deploy on Streamlit Community Cloud:

Log in to Streamlit Community Cloud.
Create a new app, selecting your GitHub repository.
Specify app.py as the main file.
Set environment variables in Streamlit Cloud's app settings:
OPENAI_API_KEY=your-api-key
BACKEND_URL=https://your-backend.onrender.com


Deploy the app. The UI will be accessible via a URL like https://your-app.streamlit.app.


Test the Deployment:

Verify that the Streamlit app communicates with the Render backend.
Upload documents and test queries to ensure functionality.



Usage

Upload Documents:
Use the Streamlit UI to upload PDFs, images (.png, .jpg, .jpeg), or text files.
A progress bar tracks upload status.


View Documents:
Uploaded documents are listed in a table with Document ID and Filename.


Ask Questions:
Enter a natural language query (e.g., "What are the penalties for non-compliance?").
Optionally exclude specific documents using the multiselect dropdown.


View Results:
Individual Answers: Displayed in a table with Document ID, Filename, Extracted Answer, and Citation.
Themes: Summarized in a chat-style format with supporting citations.



Example Output:

Table:


Document ID
Filename
Extracted Answer
Citation



DOC001
case1.pdf
The fine was imposed under section 15...
Page 4, Para 2


DOC002
case2.pdf
Delay in disclosure violated Clause 49...
Page 2, Para 1



Themes:Theme 1 – Regulatory Non-Compliance:
- DOC001, DOC002: Highlight non-compliance with SEBI Act and LODR (Page 4, Para 2; Page 2, Para 1).
Theme 2 – Penalty Justification:
- DOC001: Explicit justification of penalties (Page 4, Para 2).



Project Structure
doc-research-chatbot/
├── main.py              # FastAPI backend for document upload and query processing
├── app.py               # Streamlit frontend for UI
├── requirements.txt     # Python dependencies
├── uploads/             # Directory for uploaded files
├── chroma_db/           # ChromaDB persistence directory
└── README.md            # Project documentation

Dataset

Recommended: Use publicly available legal case PDFs from court websites (e.g., Indian Supreme Court, US Federal Courts) or synthetic legal documents.
Testing: Generate synthetic PDFs with tools like reportlab or download sample legal texts from open datasets.
Formats: Supports PDFs, images (.png, .jpg, .jpeg), and plain text (.txt).

Performance Optimizations

Parallel Processing: Uses ThreadPoolExecutor for concurrent document uploads and query searches, reducing I/O wait times.
Caching: Streamlit's @st.cache_data caches document lists and query results to avoid redundant API calls.
Async API Calls: httpx enables asynchronous HTTP requests for faster backend communication.
Progress Feedback: Progress bar for uploads and spinner for queries improve user experience.
Efficient Vector Search: ChromaDB with SentenceTransformer embeddings ensures fast semantic search.

Limitations

OCR Performance: Tesseract OCR may struggle with low-quality scans or complex layouts. Cloud-based OCR (e.g., Google Vision) could improve accuracy.
Backend Hosting: Streamlit Community Cloud cannot host FastAPI directly, requiring a separate service like Render.
Scalability: ChromaDB is suitable for small to medium datasets. For thousands of documents, consider Qdrant or a distributed vector store.
Theme Identification: Relies on OpenAI's LLM, which may introduce latency or costs for high query volumes.

Future Improvements

Advanced Filtering: Add sorting by date, author, or document type by extending ChromaDB metadata.
Visual Citation Mapping: Implement clickable links from themes to document excerpts.
Cloud OCR Integration: Replace Tesseract with Google Vision or AWS Textract for better OCR accuracy.
Distributed Search: Use Qdrant for larger-scale vector search.
Authentication: Add user authentication for multi-user support.

Contributing

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request with detailed descriptions.

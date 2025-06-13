# 📄 Document Research & Theme Identification Chatbot

A web-based chatbot that ingests 75+ documents (PDFs, images, and text), answers user queries with precise paragraph-level citations, and identifies common themes across documents.

---

## 🧠 Features

* **Document Upload**: Supports 75+ documents (PDFs, images \[.png, .jpg, .jpeg], text) with OCR for scanned images.
* **Query Processing**: Natural language queries return extracted answers from documents with paragraph-level citations (e.g., *"Page 4, Para 2"*).
* **Theme Identification**: Identifies common themes across answers with supporting citations.
* **Web Interface**: Built with Streamlit for uploading, querying, and excluding documents from search.
* **Performance Optimization**: Parallel processing, caching, and asynchronous API calls.
* **Extra Features**: Tabular answer display, document exclusion, upload progress bar, and spinners for query loading.

---

## 🛠️ Tech Stack

| Component       | Technology                                             |
| --------------- | ------------------------------------------------------ |
| **Backend**     | FastAPI                                                |
| **Frontend**    | Streamlit                                              |
| **LLM**         | OpenAI GPT-4o-mini                                     |
| **Vector DB**   | ChromaDB (SentenceTransformer embeddings)              |
| **OCR Engine**  | Tesseract OCR                                          |
| **Other Tools** | PyPDF2, Pillow, httpx, concurrent.futures              |
| **Deployment**  | Streamlit Community Cloud (Frontend), Render (Backend) |

---

## ✅ Prerequisites

* Python 3.9+
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed and added to system PATH
* OpenAI API Key
* Git
* Streamlit Community Cloud account

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/Shivan5h/Doc-Research.git
cd Doc-Research

# Install Tesseract OCR
# Ubuntu:
sudo apt-get install tesseract-ocr
# macOS:
brew install tesseract
# Windows:
# Download from https://github.com/tesseract-ocr/tesseract and add to PATH

# Install Python dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY='your-api-key'
export BACKEND_URL='http://localhost:8000'  # Use `set` on Windows
```

---

## 💻 Running Locally

### Start the Backend (FastAPI):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Start the Frontend (Streamlit):

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🌐 Deployment

### 1. Deploy FastAPI Backend on Render

* Push your project to GitHub.
* Create a web service on [Render](https://render.com/):

  * **Runtime**: Python 3
  * **Build Command**: `pip install -r requirements.txt`
  * **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
  * **Environment Variable**: `OPENAI_API_KEY=your-api-key`
* Note your Render backend URL (e.g., `https://your-backend.onrender.com`).

### 2. Update Streamlit Frontend

In `app.py`:

```python
import os
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
```

Replace API URLs with dynamic usage:

```python
response = client.get(f"{BACKEND_URL}/documents")
```

### 3. Deploy Streamlit on Community Cloud

* Ensure `app.py` and `requirements.txt` are in the root directory.
* Push updates to GitHub.
* On [Streamlit Community Cloud](https://streamlit.io/cloud), create a new app from your GitHub repo.
* Set environment variables:

  * `OPENAI_API_KEY=your-api-key`
  * `BACKEND_URL=https://your-backend.onrender.com`

---

## 📦 Usage

1. **Upload**: Drag-and-drop PDFs, text, or image files into the uploader.
2. **Query**: Enter natural language questions (e.g., *"What are the penalties for non-compliance?"*).
3. **Exclude**: Optionally exclude specific documents.
4. **Results**:

   * Individual Answers: Table showing document ID, filename, answer, and citation.
   * Themes: Summarized in chat format with references.

#### Example Output

**Answers Table:**

| Document ID | Filename  | Extracted Answer                          | Citation       |
| ----------- | --------- | ----------------------------------------- | -------------- |
| DOC001      | case1.pdf | The fine was imposed under section 15...  | Page 4, Para 2 |
| DOC002      | case2.pdf | Delay in disclosure violated Clause 49... | Page 2, Para 1 |

**Themes:**

* **Theme 1 – Regulatory Non-Compliance**: DOC001, DOC002 (SEBI Act, LODR)
* **Theme 2 – Penalty Justification**: DOC001 (Section 15, Para 2)

---

## 📁 Project Structure

```
doc-research-chatbot/
├── app.py              # Streamlit frontend
├── main.py             # FastAPI backend
├── requirements.txt    # Python dependencies
├── uploads/            # Stores uploaded files
├── chroma_db/          # ChromaDB storage
└── README.md           # Project documentation
```

---

## 📚 Dataset Recommendations

* **Legal PDFs** from court websites (Indian Supreme Court, US Federal Courts)
* **Synthetic documents** using `reportlab` or open-source legal text datasets
* Supported formats: `.pdf`, `.png`, `.jpg`, `.jpeg`, `.txt`

---

## ⚡ Performance Optimizations

* **Parallel Uploads & Queries**: `ThreadPoolExecutor`
* **Caching**: `@st.cache_data` in Streamlit for results and document metadata
* **Asynchronous Calls**: via `httpx` to backend
* **Efficient Search**: ChromaDB + SentenceTransformers for fast semantic retrieval
* **Progress Feedback**: Upload bar and spinner for user experience

---

## ⚠️ Limitations

* **OCR Quality**: Tesseract may fail on low-res or skewed images. Consider Google Vision or AWS Textract for production.
* **Scalability**: ChromaDB works best for small to medium datasets; Qdrant is recommended for larger corpora.
* **Hosting**: FastAPI backend requires external host (Render), as Streamlit Cloud only supports frontend.

---

## 🌱 Future Improvements

* Document sorting & filtering by metadata (date, type, author)
* Visual citations linked to document sections
* Replace Tesseract with advanced OCR (Google Vision, AWS Textract)
* Switch to Qdrant or Weaviate for large-scale vector search
* Add authentication for multi-user access

---

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:

   ```bash
   git commit -m "Add your feature"
   ```
4. Push and open a pull request.

---


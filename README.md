# ForecastGPT – AI-Powered Financial Outlook Agent

## 📌 Overview
ForecastGPT is an end-to-end AI system designed to analyze real quarterly financial reports and earnings call transcripts, extract key financial insights, and generate qualitative next-quarter forecasts using **Ollama + LLaMA models**, **FAISS-based RAG**, and **FastAPI**.  
Built with production-like architecture — featuring PDF processing, vector embeddings, local LLM inference, caching, and MySQL logging.

---

## 🧩 Problem Statement
Financial analysts spend hours manually:
- Reading quarterly financial PDFs  
- Extracting metrics (revenue, margins, YoY/ QoQ performance)  
- Understanding management commentary  
- Identifying risks & opportunities  
- Building qualitative forecasts  

This project **automates** the entire workflow using an AI agent powered by local models + structured RAG.

---

## 🚀 Tech Stack & Why It Was Used
### **1. FastAPI**
- High-performance API framework  
- Auto-generates Swagger UI  
- Excellent for ML-serving  

### **2. Ollama (LLaMA 3.2)**
- Run LLMs locally  
- No API costs  
- Fast inference on-device  

### **3. FAISS**
- Used for similarity search  
- Enables RAG over large PDF text chunks  
- Super fast vector indexing  

### **4. PyPDF2 / PDFPlumber**
- Extract structured PDF data  
- Handles scanned/complex PDFs  

### **5. MySQL**
- Stores logs  
- Auditable AI output  
- Demonstrates enterprise patterns  

---

## 🏗 Architecture
### **1. System Overview**
```
PDFs → Extractor → Chunker → FAISS Index → LLM Agent → Forecast Output
```

### **2. Sequence Flow**
```
User Query → Load PDFs → Cache → Embed → FAISS Search → Generate Context → LLaMA Response → Return JSON
```

### **3. RAG Flow (FAISS)**
```
Documents → Chunk → Embeddings → FAISS Index → Top-K Retrieval → Context Passed to Model
```

---

## 📁 Project Structure
```
app/
│── utils/
│   ├── fetcher.py         # Download & cache PDFs
│   ├── text.py            # PDF → text extractor & chunker
│   ├── config.py          # Settings & paths
│   ├── logger.py
│── tools/
│   ├── market_data.py     # Yahoo Finance fetcher
│── db/
│   ├── connection.py
│   ├── models.py
└── main.py                # FastAPI entrypoint
└── agent.py               # LLM agent + RAG logic
```

---

## 🧪 Features
### ✔ PDF Extraction  
### ✔ Transcript Parsing  
### ✔ Financial Trend Analysis  
### ✔ Risk & Opportunity Detection  
### ✔ Local-LLaMA Forecast Generation  
### ✔ MySQL Logging  
### ✔ Automatic Caching of PDFs  
### ✔ Clean JSON API Output  

---

## 📡 API Usage
### **Endpoint: `/forecast`**
Request example:
```json
{
  "query": "Analyze financials and provide a qualitative forecast.",
  "financial_doc_urls": [
    "https://example.com/TCS_Q3_results.pdf"
  ],
  "transcript_urls": [
    "https://example.com/TCS_Q3_transcript.pdf"
  ]
}
```

---

## 🧰 Installation & Setup
### 1️⃣ Clone repo
```
git clone <repo-url>
cd ForecastGPT
```

### 2️⃣ Create virtual env
```
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Install Ollama
https://ollama.com/download

### 5️⃣ Pull LLaMA model
```
ollama pull llama3.2
```

### 6️⃣ Start API
```
uvicorn app.main:app --reload
```

---

## 🗄 MySQL Setup
```sql
CREATE DATABASE forecastgpt;
USE forecastgpt;

CREATE TABLE forecast_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    query TEXT,
    input_meta JSON,
    output_json JSON,
    model_used VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🖼 Screenshots (Located in `/screenshots`)
1. Architecture diagram  
2. Sequence flow  
3. FAISS/RAG flow  
4. Swagger UI  
5. POST request demo  
6. MySQL log table  
7. Terminal running FastAPI  

---

## 🛡 GitHub Visibility Boosters
- Well-structured project directory  
- Clean `.gitignore`  
- Professional README  
- Architecture diagrams  
- Screenshots folder  
- LICENSE file  
- Tags for discoverability  

---

## 📜 License
MIT License

---

## 🎉 Author
**Abhay Yemekar**  
Python Developer | AI Engineer  

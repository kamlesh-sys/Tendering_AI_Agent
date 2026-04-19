# 📚 Tendering AI Search Tool (RAG + FAISS + Reranker + Ollama)

## 🚀 Project Overview
This project is an **AI-powered Tender Document Question Answering System** built using **Retrieval-Augmented Generation (RAG)**.  
It allows users to upload PDF tender documents and ask natural language questions, receiving accurate, context-grounded answers.

The system uses:
- FAISS for vector search
- SentenceTransformers for embeddings
- Cross-Encoder reranking for improved relevance
- Ollama (LLaMA 3) for answer generation
- Streamlit for UI

---

## 🧠 Key Features
- 📄 Upload and process tender PDF documents
- ✂️ Automatic text chunking from PDFs
- 🔎 Semantic search using FAISS vector database
- 🎯 Reranking using Cross-Encoder model
- 🤖 LLM-powered answer generation (Ollama LLaMA 3)
- 🧠 Anti-hallucination validation layer
- 📌 Page-level citation support
- 💬 Interactive Streamlit chat interface

---

## 🏗️ System Architecture

PDF Upload → Text Extraction → Chunking → Embeddings  
→ FAISS Index → Retrieval → Reranking → LLM (Ollama)  
→ Validation → Final Answer

---

## ⚙️ Tech Stack

- Python 🐍
- Streamlit 🎈
- FAISS (Facebook AI Similarity Search)
- SentenceTransformers
- CrossEncoder (ms-marco-MiniLM-L-6-v2)
- PyPDF
- Ollama (LLaMA 3 LLM)
- NumPy
- Requests

---

## 📂 Project Structure
```
├── app.py # Streamlit frontend UI
├── rag_agent.py # RAG backend logic (pipeline)
├── models/ # Local embedding model (MiniLM)
```


---

## 🔄 How It Works

### 1. PDF Upload
User uploads tender document in PDF format.

### 2. Chunking
Document is split into 200-word overlapping chunks.

### 3. Embeddings
Each chunk is converted into vector embeddings using:
`all-MiniLM-L6-v2`

### 4. FAISS Indexing
Embeddings are stored in FAISS for fast similarity search.

### 5. Retrieval
Top relevant chunks are fetched based on query.

### 6. Reranking
Cross-Encoder improves ranking accuracy of retrieved results.

### 7. LLM Generation
Ollama LLaMA 3 generates final answer using retrieved context.

### 8. Validation
Ensures response is grounded in document context (anti-hallucination).

---

## ▶️ How to Run Project

### 1. Install Dependencies
```bash
pip install streamlit faiss-cpu sentence-transformers pypdf requests numpy```

#start ollama server
```
ollama run llama3
```
# Run Streamlit App
```
streamlit run app.py
```
```
Application Flow
Upload Tender PDF
Ask Question
System retrieves relevant context
Reranks best answers
LLM generates final response
Displays grounded answer with page reference
📊 Example Queries
What are the eligibility criteria in this tender?
What is the submission deadline?
What documents are required?
What is the scope of work?
🧠 Key AI Concepts Used
Retrieval-Augmented Generation (RAG)
Vector Embeddings
Semantic Search
Reranking (Cross-Encoder)
Large Language Models (LLM)
Agentic AI Pipeline Design
Prompt Engineering
Context Grounding & Hallucination Control
🛡️ Safety Features
Answer restricted only to document context
If context missing → returns "Insufficient context"
Validation layer prevents hallucinated answers
Page-level citation support
📌 Future Improvements
Multi-document RAG support
Chat history memory
Cloud deployment (AWS / Azure)
Advanced reranker (bigger model)
UI dashboard for analytics
Role-based access (Govt/Private tender system)
```


Tendering AI Search Tool (RAG + FAISS + Ollama)

An intelligent Retrieval-Augmented Generation (RAG) system designed to analyze tender documents (PDFs) and answer user queries with context-aware, citation-backed responses.

Built using Streamlit, FAISS, Sentence Transformers, and Ollama (LLM).

🚀 Features
📄 Upload and process tender PDF documents
🔍 Semantic search using FAISS vector database
🧠 Reranking using Cross-Encoder for better relevance
🤖 LLM-powered answers using Ollama (Llama3)
✅ Anti-hallucination validation mechanism
📌 Page-wise citation in answers
⚡ Fast and interactive UI with Streamlit
🏗️ System Architecture
PDF → Chunking → Embeddings → FAISS Index
        ↓
     Query → Retrieval → Reranking → LLM (Ollama)
                                ↓
                         Final Answer (Validated)
🛠️ Tech Stack
Frontend: Streamlit
Backend: Python
Vector DB: FAISS
Embeddings: all-MiniLM-L6-v2
Reranker: Cross-Encoder (MS MARCO)
LLM: Ollama (Llama3)
PDF Processing: PyPDF
📂 Project Structure
AIProject/
│── app.py                # Streamlit UI
│── rag_agent.py          # RAG pipeline logic
│── download_model.py     # Download embedding model
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
│── codes_folder/         # Additional scripts
⚙️ Setup Instructions
1️⃣ Clone Repository
git clone https://github.com/your-username/Tendering_AI_Agent.git
cd Tendering_AI_Agent
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Download Embedding Model
python download_model.py
5️⃣ Start Ollama (LLM Server)

Install Ollama and run:

ollama serve

Then pull model:

ollama pull llama3
6️⃣ Run Application
streamlit run app.py
🧠 How It Works
🔹 Step 1: PDF Processing
Extracts text from uploaded PDF
Splits into chunks (200 words each)
🔹 Step 2: Embedding & Indexing
Converts text into vector embeddings
Stores in FAISS index for fast similarity search
🔹 Step 3: Query Processing
User query is embedded
Top-k relevant chunks retrieved
🔹 Step 4: Reranking
Cross-encoder ranks results for accuracy
🔹 Step 5: LLM Generation
Context + query sent to Ollama (Llama3)
Generates concise answer
🔹 Step 6: Validation
Ensures answer is grounded in document
Prevents hallucination
⚠️ Important Notes
Models (models/, googl-flan-t5-base/) are not included in repo
Ollama must be running locally (localhost:11434)
Works best with text-based PDFs (not scanned images)
📌 Example Use Cases
📑 Tender document analysis
📊 Policy document Q&A
📘 UPSC / academic document assistant
🏢 Enterprise knowledge retrieval
🚧 Limitations
Does not support scanned PDFs (no OCR)
Depends on local LLM (Ollama)
Large PDFs may take time to process
🔮 Future Improvements
Add OCR support for scanned PDFs
Deploy on cloud (AWS/GCP)
Add multi-document support
Improve UI/UX
Integrate LangGraph multi-agent system
👨‍💻 Author

Kamlesh Kumar
IIT Madras – BS in Data Science

⭐ Acknowledgements
Sentence Transformers
FAISS
Ollama
Streamlit
📜 License

This project is licensed under the MIT License.
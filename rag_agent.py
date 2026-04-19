import streamlit as st
import numpy as np
import faiss
import requests
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, CrossEncoder

# =========================
# MODELS
# =========================
embed_model = SentenceTransformer(r"C:\AIProject\models\all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"

# =========================
# STREAMLIT STATE INIT (CRITICAL FIX)
# =========================
if "chunks" not in st.session_state:
    st.session_state.chunks = None

if "index" not in st.session_state:
    st.session_state.index = None


# =========================
# PDF PROCESSING
# =========================
def process_pdf(file):
    reader = PdfReader(file)
    chunks = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if not text.strip():
            continue

        words = text.split()
        chunk_size = 200

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i+chunk_size])
            chunks.append({
                "text": chunk,
                "page": page_num
            })

    return chunks


# =========================
# BUILD FAISS INDEX
# =========================
def build_index(chunks):
    texts = [c["text"] for c in chunks]

    embeddings = embed_model.encode(texts, normalize_embeddings=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(np.array(embeddings).astype("float32"))

    return index


# =========================
# LOAD DATA INTO SESSION
# =========================
def load_and_store(file):
    chunks = process_pdf(file)
    index = build_index(chunks)

    st.session_state.chunks = chunks
    st.session_state.index = index

    return f"✅ Loaded {len(chunks)} chunks from PDF"


# =========================
# RETRIEVAL (SAFE)
# =========================
def retrieve(query, k=8):
    if st.session_state.index is None:
        return []

    q_emb = embed_model.encode([query], normalize_embeddings=True)

    scores, idxs = st.session_state.index.search(
        np.array(q_emb).astype("float32"), k
    )

    return [st.session_state.chunks[i] for i in idxs[0]]


# =========================
# RERANKING
# =========================
def rerank(query, docs, k=3):
    if not docs:
        return []

    pairs = [(query, d["text"]) for d in docs]
    scores = reranker.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [r[0] for r in ranked[:k]]


# =========================
# VALIDATION (ANTI-HALLUCINATION)
# =========================
def validate(answer, docs):
    context = " ".join([d["text"].lower() for d in docs])
    answer = answer.lower()

    overlap = sum(1 for w in answer.split() if w in context)
    return overlap >= 5


# =========================
# OLLAMA CALL
# =========================
def call_llm(prompt):
    res = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })

    return res.json()["response"]


# =========================
# RAG PIPELINE
# =========================
def run_rag(query):
    docs = retrieve(query)
    docs = rerank(query, docs)

    if not docs:
        return "⚠️ Please upload a PDF first."

    context = "\n\n".join(
        [f"(Page {d['page']}) {d['text']}" for d in docs]
    )

    prompt = f"""
You are a UPSC exam assistant.

RULES:
- Use ONLY the provided context
- If answer not present → say "Insufficient context"
- Add page citations like (Page X)
- Be concise and exam-ready

CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

    answer = call_llm(prompt)

    if not validate(answer, docs):
        return "❌ Answer not grounded in document. Try rephrasing."

    return answer


# =========================
# CLASS ENTRYPOINT
# =========================
class RAGApp:

    def load_data(self, file):
        return load_and_store(file)

    def invoke(self, state):
        return {"final_answer": run_rag(state["query"])}


app = RAGApp()
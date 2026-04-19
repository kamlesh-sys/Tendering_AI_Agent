# -------------------- PDF LOADING --------------------
from pypdf import PdfReader

def load_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


file_path = r"C:\AIProject\MW-GS1-MODERN-HISTORY.pdf"
pdf_text = load_pdf(file_path)


# -------------------- CHUNKING --------------------
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = splitter.split_text(pdf_text)


# -------------------- EMBEDDINGS + FAISS --------------------
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

embeddings = embed_model.encode(chunks)

embeddings = np.array(embeddings).astype("float32")

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)


# -------------------- QUERY --------------------
query = "approach to prepare modern history for upsc?"

query_vec = embed_model.encode([query]).astype("float32")


# -------------------- RETRIEVAL --------------------
D, I = index.search(query_vec, k=3)

retrieved_docs = [chunks[i] for i in I[0]]


# -------------------- SIMPLE LLM (FIXED) --------------------
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

model_name = "google/flan-t5-base"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def llm(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# -------------------- RAG PROMPT --------------------
context = "\n".join(retrieved_docs)

prompt = f"""
Answer using ONLY this context:

{context}

Question: {query}
"""

answer = llm(prompt)

print("ANSWER:\n", answer)
import streamlit as st
from rag_agent import app

st.set_page_config(page_title="TENDERING AI Agent")

st.title("📚 TENDERING AI SEARCH TOOL (FAISS + Reranker + Ollama)")

# =========================
# UPLOAD PDF
# =========================
uploaded_file = st.file_uploader("Upload TENDER DOCUMENTS IN PDF", type=["pdf"])

if uploaded_file:
    msg = app.load_data(uploaded_file)
    st.success(msg)

# =========================
# QUESTION INPUT
# =========================
query = st.text_input("Ask your question:")

if st.button("Search") and query:
    with st.spinner("Thinking..."):
        result = app.invoke({"query": query})

    st.markdown("### Answer")
    st.write(result["final_answer"])
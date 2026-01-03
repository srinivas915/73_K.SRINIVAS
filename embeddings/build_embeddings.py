import json
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def main():
    with open("data/processed/chunked_documents.json", "r") as f:
        docs = json.load(f)

    texts = [d["text"] for d in docs]
    metadatas = [d["metadata"] for d in docs]

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

    os.makedirs("embeddings/vector_store/faiss", exist_ok=True)
    vectorstore.save_local("embeddings/vector_store/faiss")

    print("✅ FAISS index created")

if __name__ == "__main__":
    main()

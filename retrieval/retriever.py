from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

class Retriever:
    def __init__(self):
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.db = FAISS.load_local(
            "embeddings/vector_store/faiss",
            embeddings,
            allow_dangerous_deserialization=True
        )

    def retrieve(self, query, k=5):
        return self.db.similarity_search(query, k=k)

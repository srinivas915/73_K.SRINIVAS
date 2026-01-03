from langchain_core.prompts import PromptTemplate

RAG_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a Telecom Customer Support AI.

Use ONLY the information in the context.
If unsure, clearly say you don't know.

Context:
{context}

Question:
{question}

Answer:
"""
)

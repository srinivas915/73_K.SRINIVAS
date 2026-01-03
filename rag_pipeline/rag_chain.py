import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from retrieval.retriever import Retriever
from retrieval.advanced_confidence import compute_advanced_confidence
from rag_pipeline.advanced_handler import detect_intent, is_low_information_query

load_dotenv()

class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            temperature=0,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    def run(self, question):
        intent = detect_intent(question)

        # ---- INTENT HANDLING ----
        if intent == "GREETING":
            return {
                "answer": "Hello! 👋 How can I assist you with your telecom service today?",
                "confidence": 1.0,
                "sources": []
            }

        if intent == "THANKS":
            return {
                "answer": "You're welcome! 😊 If you have any telecom-related questions, feel free to ask.",
                "confidence": 1.0,
                "sources": []
            }

        if intent == "EXIT":
            return {
                "answer": "Thank you for contacting Telecom Support. Have a great day!",
                "confidence": 1.0,
                "sources": []
            }

        if intent == "INVALID":
            return {
                "answer": "Could you please describe your telecom issue in more detail?",
                "confidence": 0.2,
                "sources": []
            }

        # ---- QUERY QUALITY CHECK ----
        if is_low_information_query(question):
            return {
                "answer": (
                    "I need a bit more detail to help you effectively.\n\n"
                    "For example:\n"
                    "- Is the issue related to billing, network, SIM, or internet speed?\n"
                    "- When did the problem start?"
                ),
                "confidence": 0.3,
                "sources": []
            }

        # ---- RETRIEVAL ----
        docs = self.retriever.retrieve(question, k=5)

        if not docs:
            return {
                "answer": (
                    "I couldn’t find relevant historical cases for this issue.\n"
                    "I recommend escalating this to a human support agent."
                ),
                "confidence": 0.0,
                "sources": []
            }

        context = "\n\n".join(d.page_content for d in docs)

        prompt = f"""
You are a senior Telecom Technical Support AI.

RULES:
- Use ONLY the context provided.
- Do NOT guess or hallucinate.
- If information is missing, say so clearly.
- Provide steps in bullet points if applicable.
- Be concise and professional.

Context:
{context}

Customer Question:
{question}

Final Answer:
"""

        response = self.llm.invoke(prompt)

        # Extract Gemini text
        if isinstance(response.content, list):
            answer_text = response.content[0]["text"]
        else:
            answer_text = response.content

        confidence = compute_advanced_confidence(docs, answer_text)

        # ---- ESCALATION DECISION ----
        if confidence < 0.4:
            answer_text += (
                "\n\n⚠️ This issue may require human assistance. "
                "I recommend escalating this to a telecom support agent."
            )

        return {
            "answer": answer_text,
            "confidence": confidence,
            "sources": [d.metadata for d in docs]
        }

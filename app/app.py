from rag_pipeline.rag_chain import RAGPipeline
from escalation.escalation_handler import check_escalation

def main():
    rag = RAGPipeline()

    print("📞 Telecom Gemini RAG Agent (type 'exit')\n")

    while True:
        query = input("Customer: ")
        if query.lower() == "exit":
            break

        response = rag.run(query)

        print("\n🤖 Response:")
        print(response["answer"])
        print("Confidence:", response["confidence"])

        if check_escalation(response):
            print("🚨 Escalate to human agent")

        print("-" * 50)

if __name__ == "__main__":
    main()

import json
import pandas as pd
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def main():
    input_path = "data/processed/cleaned_data.csv"
    output_path = "data/processed/chunked_documents.json"

    df = pd.read_csv(input_path)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    documents = []
    doc_id = 0

    for _, row in df.iterrows():
        chunks = splitter.split_text(row["clean_text"])
        for chunk in chunks:
            documents.append({
                "id": f"doc_{doc_id}",
                "text": chunk,
                "metadata": {
                    "topic": row.get("AgentAssignedTopic", "unknown"),
                    "location": row.get("Location", "unknown"),
                    "source": "telecom_dataset"
                }
            })
            doc_id += 1

    os.makedirs("data/processed", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2)

    print("✅ chunked_documents.json generated")

if __name__ == "__main__":
    main()

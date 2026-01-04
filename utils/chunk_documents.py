import json
import pandas as pd
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

INPUT_PATH = "data/processed/cleaned_data.csv"
OUTPUT_PATH = "data/processed/chunked_documents.json"

def main():
    df = pd.read_csv(INPUT_PATH)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    all_chunks = []

    for _, row in df.iterrows():
        text = row["text"]
        source = row.get("source", "unknown")

        chunks = splitter.split_text(text)

        for chunk in chunks:
            all_chunks.append({
                "text": chunk,
                "metadata": {
                    "source": source
                }
            })

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print("✅ chunked_documents.json generated using BOTH datasets")

if __name__ == "__main__":
    main()
import pandas as pd
import os
import re

RAW_DIR = "data/raw"
OUT_PATH = "data/processed/cleaned_data.csv"

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def process_telecom():
    df = pd.read_csv(f"{RAW_DIR}/telecom_customer_interactions.csv")

    df["text"] = df["CustomerInteractionRawText"].apply(clean_text)
    df["source"] = "telecom_call"

    return df[["text", "source"]]

def process_tickets():
    df = pd.read_csv(f"{RAW_DIR}/customer_support_tickets.csv")

    df["text"] = (
        "product: " + df["Product Purchased"].fillna("") + " | " +
        "type: " + df["Ticket Type"].fillna("") + " | " +
        "subject: " + df["Ticket Subject"].fillna("") + " | " +
        "issue: " + df["Ticket Description"].fillna("") + " | " +
        "resolution: " + df["Resolution"].fillna("")
    )

    df["text"] = df["text"].apply(clean_text)
    df["source"] = "support_ticket"

    return df[["text", "source"]]

def main():
    telecom_df = process_telecom()
    ticket_df = process_tickets()

    combined = pd.concat([telecom_df, ticket_df], ignore_index=True)
    combined.to_csv(OUT_PATH, index=False)

    print("✅ cleaned_data.csv generated using BOTH datasets")

if __name__ == "__main__":
    main()

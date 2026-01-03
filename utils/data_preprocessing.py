import pandas as pd
import re
import os

def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def main():
    input_path = "data/raw/telecom_customer_interactions.csv"
    output_dir = "data/processed"
    output_path = os.path.join(output_dir, "cleaned_data.csv")

    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(input_path)

    # ✅ CORRECT COLUMN NAME
    TEXT_COLUMN = "CustomerInteractionRawText"

    df["clean_text"] = df[TEXT_COLUMN].astype(str).apply(clean_text)

    # remove empty rows
    df = df[df["clean_text"].str.len() > 10]

    df.to_csv(output_path, index=False)
    print("✅ cleaned_data.csv generated successfully")

if __name__ == "__main__":
    main()

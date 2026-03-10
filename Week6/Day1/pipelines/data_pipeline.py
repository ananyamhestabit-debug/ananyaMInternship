import pandas as pd
import os

RAW_PATH = "data/raw/customer_churn.csv"
PROCESSED_PATH = "data/processed/final.csv"


def load_data():
    df = pd.read_csv(RAW_PATH)
    print("Dataset loaded")
    return df


def remove_duplicates(df):
    df = df.drop_duplicates()
    print("Duplicates removed")
    return df


def handle_missing(df):
    df = df.fillna(df.mean(numeric_only=True))
    print("Missing values handled")
    return df


def save_data(df):
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print("Processed dataset saved")


def run_pipeline():
    df = load_data()
    df = remove_duplicates(df)
    df = handle_missing(df)
    save_data(df)


if __name__ == "__main__":
    run_pipeline()
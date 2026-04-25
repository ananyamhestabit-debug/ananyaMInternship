import pandas as pd
import os

def run_data_pipeline():
    df = pd.read_csv("data/raw/titanic.csv")

    df = df.drop_duplicates()

    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/final.csv", index=False)

    print("final.csv recreated correctly")

if __name__ == "__main__":
    run_data_pipeline()
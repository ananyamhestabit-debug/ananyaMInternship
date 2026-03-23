import pandas as pd
import numpy as np
import os

RAW_PATH = "data/raw/titanic.csv"
PROCESSED_PATH = "data/processed/final.csv"

#loads data
def load_data():
    df = pd.read_csv(RAW_PATH)
    print("Data loaded:", df.shape)
    return df


#cleans data
def clean_data(df):

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())

    # Drop useless columns
    df = df.drop(columns=["Name", "Ticket", "Cabin"], errors="ignore")

    return df


#outlier handeling
def remove_outliers(df):

    Q1 = df["Fare"].quantile(0.25)
    Q3 = df["Fare"].quantile(0.75)
    IQR = Q3 - Q1

    df = df[(df["Fare"] >= Q1 - 1.5 * IQR) & (df["Fare"] <= Q3 + 1.5 * IQR)]

    return df

#save data
def save_data(df):

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print("Processed data saved")


#pipeline
def run_pipeline():

    df = load_data()
    df = clean_data(df)
    df = remove_outliers(df)
    save_data(df)

    print("Data pipeline completed")


if __name__ == "__main__":
    run_pipeline()
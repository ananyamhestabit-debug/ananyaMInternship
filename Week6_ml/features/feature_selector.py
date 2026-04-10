import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import json
import os

DATA_PATH = "data/processed/final.csv"
OUTPUT_PATH = "data/processed/"

os.makedirs("features", exist_ok=True)

def load_data():
    return pd.read_csv(DATA_PATH)

def create_features(df):
    df = df.copy()

    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
    df["FarePerPerson"] = df["Fare"] / df["FamilySize"]

    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 12, 18, 35, 60, 100],
        labels=["Child", "Teen", "Young", "Adult", "Senior"]
    )

    df["Title"] = df["Name"].str.extract(r' ([A-Za-z]+)\.', expand=False)
    df["Deck"] = df["Cabin"].astype(str).str[0]
    df["TicketLength"] = df["Ticket"].astype(str).apply(len)

    df["LogFare"] = np.log1p(df["Fare"])
    df["AgeClass"] = df["Age"] * df["Pclass"]
    df["FareClass"] = df["Fare"] * df["Pclass"]

    return df

def encode(df):
    df["Sex"] = LabelEncoder().fit_transform(df["Sex"])
    df = pd.get_dummies(df, columns=["Embarked", "Title", "Deck", "AgeGroup"], drop_first=True)
    return df

def scale(X):
    scaler = StandardScaler()
    X[X.columns] = scaler.fit_transform(X)
    joblib.dump(scaler, "features/scaler.pkl")
    return X

def run():
    df = load_data()

    df = create_features(df)

    df.drop(["Name", "Ticket", "Cabin"], axis=1, inplace=True, errors="ignore")

    df = encode(df)

    y = df["Survived"]
    X = df.drop("Survived", axis=1)

    X = scale(X)f_raw.hist(figsize=(12,8)) 

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train.to_csv("data/processed/X_train.csv", index=False)
    X_test.to_csv("data/processed/X_test.csv", index=False)
    y_train.to_csv("data/processed/y_train.csv", index=False)
    y_test.to_csv("data/processed/y_test.csv", index=False)

    with open("features/feature_list.json", "w") as f:
        json.dump(list(X.columns), f, indent=4)

    print("Day 2 feature engineering done")

if __name__ == "__main__":
    run()
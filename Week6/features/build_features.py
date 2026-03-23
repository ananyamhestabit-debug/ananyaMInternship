import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

DATA_PATH = "data/processed/final.csv"

#load data
def load_data():
    return pd.read_csv(DATA_PATH)


#feature creation
def create_features(df):

    df["FamilySize"] = df["SibSp"] + df["Parch"]

    df["IsAlone"] = (df["FamilySize"] == 0).astype(int)

    df["Fare_per_person"] = df["Fare"] / (df["FamilySize"] + 1)

    df["Age_log"] = np.log1p(df["Age"])

    df["Fare_log"] = np.log1p(df["Fare"])

    df["Age_squared"] = df["Age"] ** 2

    df["Fare_squared"] = df["Fare"] ** 2

    df["Age_Fare_product"] = df["Age"] * df["Fare"]

    df["Pclass_Fare"] = df["Pclass"] * df["Fare"]

    df["Age_bin"] = pd.cut(df["Age"], bins=5, labels=False)

    return df


#encoding
def encode_data(X):

    cat_cols = X.select_dtypes(include=["object", "string"]).columns

    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")

    encoded = encoder.fit_transform(X[cat_cols])

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(cat_cols)
    )

    X = X.drop(columns=cat_cols)

    X = pd.concat([X.reset_index(drop=True), encoded_df], axis=1)

    return X


#scaling
def scale_data(X):

    scaler = StandardScaler()

    num_cols = X.select_dtypes(include=["int64", "float64"]).columns

    X[num_cols] = scaler.fit_transform(X[num_cols])

    return X


#pipeline
def run_feature_pipeline():

    df = load_data()

    # separates target 
    y = df["Survived"]

    # drop target plus useless column
    X = df.drop(columns=["Survived", "PassengerId"], errors="ignore")

    X = create_features(X)
    X = encode_data(X)
    X = scale_data(X)

    return train_test_split(X, y, test_size=0.2, random_state=42)

if __name__ == "__main__":

    X_train, X_test, y_train, y_test = run_feature_pipeline()

    print("Feature pipeline completed")
    print("Train shape:", X_train.shape)
import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

DATA_PATH = "data/processed/final.csv"


def load_data():

    df = pd.read_csv(DATA_PATH)

    # Convert TotalCharges to numeric
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

    # Fill missing values
    df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

    return df


def create_new_features(df):

    df["charges_per_tenure"] = df["MonthlyCharges"] / (df["tenure"] + 1)

    df["tenure_years"] = df["tenure"] / 12

    df["avg_monthly_spend"] = df["TotalCharges"] / (df["tenure"] + 1)

    df["high_value_customer"] = (df["MonthlyCharges"] > 70).astype(int)

    df["long_term_customer"] = (df["tenure"] > 24).astype(int)

    df["charge_log"] = np.log1p(df["MonthlyCharges"])

    df["tenure_sqrt"] = np.sqrt(df["tenure"])

    df["charges_squared"] = df["MonthlyCharges"] ** 2

    df["tenure_squared"] = df["tenure"] ** 2

    df["charges_tenure_product"] = df["MonthlyCharges"] * df["tenure"]

    return df


def encode_categorical(df):

    # Select categorical columns
    categorical_cols = df.select_dtypes(include=["object", "string"]).columns

    encoder = OneHotEncoder(
        sparse_output=False,
        handle_unknown="ignore"
    )

    encoded = encoder.fit_transform(df[categorical_cols])

    encoded_df = pd.DataFrame(
        encoded,
        columns=encoder.get_feature_names_out(categorical_cols)
    )

    df = df.drop(columns=categorical_cols)

    df = pd.concat([df.reset_index(drop=True), encoded_df], axis=1)

    return df


def normalize_features(df):

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    scaler = StandardScaler()

    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df


def split_data(df):

    y = df["Churn_Yes"]

    X = df.drop(columns=["Churn_Yes"])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    return X_train, X_test, y_train, y_test


def run_feature_pipeline():

    df = load_data()

    df = create_new_features(df)

    df = encode_categorical(df)

    df = normalize_features(df)

    X_train, X_test, y_train, y_test = split_data(df)

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":

    X_train, X_test, y_train, y_test = run_feature_pipeline()

    print("Feature pipeline completed")

    print("Train shape:", X_train.shape)
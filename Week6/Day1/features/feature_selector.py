import pandas as pd
import numpy as np
import json

from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier

from build_features import run_feature_pipeline


def correlation_filter(X, threshold=0.9):

    print("Running correlation filter...")

    corr_matrix = X.corr().abs()

    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )

    to_drop = [col for col in upper.columns if any(upper[col] > threshold)]

    X_filtered = X.drop(columns=to_drop)

    print("After correlation filter:", X_filtered.shape[1])

    return X_filtered


def mutual_information_selection(X, y, top_k=100):

    print("Running mutual information...")

    y = pd.Series(y).astype(int)

    mi = mutual_info_classif(X, y)

    mi_series = pd.Series(mi, index=X.columns)

    mi_series = mi_series.sort_values(ascending=False)

    selected_features = mi_series.head(top_k).index.tolist()

    print("After mutual information:", len(selected_features))

    return selected_features


def rfe_selection(X, y, n_features=30):

    print("Running RFE...")

    model = RandomForestClassifier(
        n_estimators=50,
        random_state=42,
        n_jobs=-1
    )

    rfe = RFE(model, n_features_to_select=n_features, step=10)

    rfe.fit(X, y)

    selected_features = X.columns[rfe.support_].tolist()

    print("After RFE:", len(selected_features))

    return selected_features


def run_feature_selection():

    print("Loading feature pipeline...")

    X_train, X_test, y_train, y_test = run_feature_pipeline()

    y_train = pd.Series(y_train).astype(int)

    print("Initial features:", X_train.shape[1])

    # Step 1: correlation filter
    X_filtered = correlation_filter(X_train)

    # Step 2: mutual information
    selected_mi = mutual_information_selection(X_filtered, y_train)

    X_mi = X_filtered[selected_mi]

    # Step 3: RFE
    final_features = rfe_selection(X_mi, y_train)

    # save feature list
    with open("features/feature_list.json", "w") as f:
        json.dump(final_features, f, indent=4)

    print("Feature selection completed")
    print("Final selected features:", len(final_features))


if __name__ == "__main__":
    run_feature_selection()
import pandas as pd
import numpy as np
import json

from sklearn.feature_selection import mutual_info_regression
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestRegressor

from build_features import run_feature_pipeline


def correlation_filter(X, threshold=0.9):

    corr_matrix = X.corr().abs()

    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )

    to_drop = [column for column in upper.columns if any(upper[column] > threshold)]

    X_filtered = X.drop(columns=to_drop)

    print("After correlation filter:", X_filtered.shape[1])

    return X_filtered


def mutual_information_selection(X, y, top_k=200):

    mi = mutual_info_regression(X, y)

    mi_series = pd.Series(mi, index=X.columns)

    mi_series = mi_series.sort_values(ascending=False)

    selected_features = mi_series.head(top_k).index.tolist()

    print("After mutual information:", len(selected_features))

    return selected_features


def rfe_selection(X, y, n_features=50):

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    rfe = RFE(model, n_features_to_select=n_features)

    rfe.fit(X, y)

    selected_features = X.columns[rfe.support_].tolist()

    print("After RFE:", len(selected_features))

    return selected_features


def run_feature_selection():

    print("Loading feature pipeline...")

    X_train, X_test, y_train, y_test = run_feature_pipeline()

    print("Initial features:", X_train.shape[1])

    X_filtered = correlation_filter(X_train)

    selected_mi = mutual_information_selection(X_filtered, y_train)

    X_mi = X_filtered[selected_mi]

    final_features = rfe_selection(X_mi, y_train)

    with open("selected_features.json", "w") as f:
        json.dump(final_features, f)

    print("Feature selection completed")
    print("Final selected features:", len(final_features))


if __name__ == "__main__":
    run_feature_selection()
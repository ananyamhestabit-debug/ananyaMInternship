import pandas as pd
import json

from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel

from build_features import run_feature_pipeline


def run_feature_selection():

    print("Loading feature pipeline...")

    X_train, X_test, y_train, y_test = run_feature_pipeline()

    print("Initial features:", X_train.shape[1])

#mutual info
    mi = mutual_info_classif(X_train, y_train)

    mi_series = pd.Series(mi, index=X_train.columns)

    selected = mi_series.sort_values(ascending=False).head(15).index.tolist()

    print("Top features (MI):", len(selected))

    X_selected = X_train[selected]

#model based selection
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    model.fit(X_selected, y_train)

    selector = SelectFromModel(model, prefit=True)

    final_features = X_selected.columns[selector.get_support()].tolist()

    print("Final selected features:", len(final_features))

#saves features
    with open("features/feature_list.json", "w") as f:
        json.dump(final_features, f, indent=4)

    print("Feature list saved")


if __name__ == "__main__":
    run_feature_selection()
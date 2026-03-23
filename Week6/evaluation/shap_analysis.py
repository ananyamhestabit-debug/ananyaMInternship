import sys
import os
import shap
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from features.build_features import run_feature_pipeline
from sklearn.ensemble import RandomForestClassifier

def feature_importance(model, X):

    importances = model.feature_importances_

    plt.figure(figsize=(8,6))
    plt.barh(X.columns, importances)

    plt.title("Feature Importance")

    os.makedirs("evaluation", exist_ok=True)
    plt.savefig("evaluation/feature_importance.png")
    plt.close()

    print("Feature importance saved")

def error_analysis(model, X, y):

    preds = model.predict(X)

    cm = confusion_matrix(y, preds)

    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt="d")

    plt.title("Error Analysis")

    os.makedirs("evaluation", exist_ok=True)
    plt.savefig("evaluation/error_heatmap.png")
    plt.close()

    print("Error analysis saved")


def run_shap():

    print("Loading data...")

    #Load data
    X_train, X_test, y_train, y_test = run_feature_pipeline()

    #Load selected features
    with open("features/feature_list.json") as f:
        features = json.load(f)

    X_train = X_train[features]

#Train tuned RandomForest
    print("Training model...")

    model = RandomForestClassifier(
        n_estimators=85,
        max_depth=8,
        min_samples_split=4,
        random_state=42
    )

    model.fit(X_train, y_train)

#SHAP
    print("Running SHAP...")

    explainer = shap.Explainer(model, X_train)
    shap_values = explainer(X_train)

    shap.summary_plot(shap_values, X_train, show=False)

    os.makedirs("evaluation", exist_ok=True)
    plt.savefig("evaluation/shap_summary.png")
    plt.close()

    print("SHAP completed")

#Feature importance
    feature_importance(model, X_train)

#Error analysis
    error_analysis(model, X_train, y_train)

if __name__ == "__main__":
    run_shap()
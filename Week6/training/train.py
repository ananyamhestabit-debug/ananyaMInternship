import sys
import os
import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#fixes import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

from features.build_features import run_feature_pipeline


#loads selected features
def load_features():
    with open("features/feature_list.json") as f:
        return json.load(f)


#evaluates model
def evaluate_model(model, X, y):

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    predictions = cross_val_predict(model, X, y, cv=cv)

    probabilities = cross_val_predict(model, X, y, cv=cv, method="predict_proba")[:, 1]

    metrics = {}

    metrics["accuracy"] = accuracy_score(y, predictions)
    metrics["precision"] = precision_score(y, predictions)
    metrics["recall"] = recall_score(y, predictions)
    metrics["f1"] = f1_score(y, predictions)
    metrics["roc_auc"] = roc_auc_score(y, probabilities)

    cm = confusion_matrix(y, predictions)

    return metrics, cm

#training pipleline
def train_models():

    print("Loading data...")

    X_train, X_test, y_train, y_test = run_feature_pipeline()

    selected_features = load_features()

    X_train = X_train[selected_features]

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(
            n_estimators=85,
        max_depth=8,
        min_samples_split=4,
        random_state=42
),
        "XGBoost": XGBClassifier(eval_metric="logloss"),
        "NeuralNetwork": MLPClassifier(hidden_layer_sizes=(64,32), max_iter=300)
    }

    results = {}

    best_score = 0
    best_model = None
    best_model_name = None
    best_cm = None

    for name, model in models.items():

        print(f"Training {name}...")

        metrics, cm = evaluate_model(model, X_train, y_train)

        results[name] = metrics

        if metrics["f1"] > best_score:
            best_score = metrics["f1"]
            best_model = model
            best_model_name = name
            best_cm = cm

    print("Best model:", best_model_name)

#train best model fully
    best_model.fit(X_train, y_train)

#save model
    os.makedirs("models", exist_ok=True)
    joblib.dump(best_model, "models/best_model.pkl")

#save metrics
    os.makedirs("evaluation", exist_ok=True)
    with open("evaluation/metrics.json", "w") as f:
        json.dump(results, f, indent=4)

#save confusion matrix
    plt.figure(figsize=(5,4))
    sns.heatmap(best_cm, annot=True, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix")
    plt.savefig("evaluation/confusion_matrix.png")
    plt.close()

    print("Training completed")


if __name__ == "__main__":
    train_models()
import pandas as pd
import json
import joblib
import os

from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier


# load data
X = pd.read_csv("data/processed/X_train.csv")
y = pd.read_csv("data/processed/y_train.csv").values.ravel()

os.makedirs("models", exist_ok=True)
os.makedirs("evaluation", exist_ok=True)


# define models
models = {
    "logistic": LogisticRegression(max_iter=1000),
    "random_forest": RandomForestClassifier(),
    "neural_network": MLPClassifier(max_iter=500)
}


results = {}
best_score = 0
best_model = None
best_model_name = ""


# train and evaluate
for name, model in models.items():

    # cross validation
    cv_scores = cross_val_score(model, X, y, cv=5)

    # fit model
    model.fit(X, y)

    # predictions
    preds = model.predict(X)

    # metrics
    acc = accuracy_score(y, preds)
    prec = precision_score(y, preds)
    rec = recall_score(y, preds)
    f1 = f1_score(y, preds)
    roc = roc_auc_score(y, preds)

    # confusion matrix
    cm = confusion_matrix(y, preds).tolist()

    results[name] = {
        "cv_mean": cv_scores.mean(),
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1_score": f1,
        "roc_auc": roc,
        "confusion_matrix": cm
    }

    # select best model (based on f1)
    if f1 > best_score:
        best_score = f1
        best_model = model
        best_model_name = name


# save best model
joblib.dump(best_model, "models/best_model.pkl")

# save metrics
with open("evaluation/metrics.json", "w") as f:
    json.dump(results, f, indent=4)


print("training completed")
print("best model:", best_model_name)
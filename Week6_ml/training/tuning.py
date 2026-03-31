import pandas as pd
import json
import os

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier

# load data
X = pd.read_csv("data/processed/X_train.csv")
y = pd.read_csv("data/processed/y_train.csv").values.ravel()

# ensure folder exists
os.makedirs("tuning", exist_ok=True)

print("data loaded")

# model
model = RandomForestClassifier()

# parameters
params = {
    "n_estimators": [50, 100],
    "max_depth": [3, 5, None]
}

print("starting grid search")

# grid search
grid = GridSearchCV(model, params, cv=3, scoring="f1")
grid.fit(X, y)

print("grid search done")

# save results
with open("tuning/results.json", "w") as f:
    json.dump(grid.best_params_, f, indent=4)

print("results saved:", grid.best_params_)
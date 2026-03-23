import sys
import os
import optuna
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

from features.build_features import run_feature_pipeline
#loads data
def load_data():

    X_train, X_test, y_train, y_test = run_feature_pipeline()

    with open("features/feature_list.json") as f:
        features = json.load(f)

    X_train = X_train[features]

    return X_train, y_train


X_train, y_train = load_data()

def objective(trial):

    model = RandomForestClassifier(
        n_estimators=trial.suggest_int("n_estimators", 50, 150),
        max_depth=trial.suggest_int("max_depth", 3, 10),
        min_samples_split=trial.suggest_int("min_samples_split", 2, 10),
        random_state=42
    )

    score = cross_val_score(model, X_train, y_train, cv=3, scoring="f1").mean()

    return score


#runs tuning
def run_tuning():

    study = optuna.create_study(direction="maximize")

    study.optimize(objective, n_trials=5)

    best_params = study.best_params

    print("Best Parameters:", best_params)

    os.makedirs("tuning", exist_ok=True)

    with open("tuning/results.json", "w") as f:
        json.dump(best_params, f, indent=4)



if __name__ == "__main__":
    run_tuning()
import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import os

# create folder
os.makedirs("evaluation", exist_ok=True)

# load model and data
model = joblib.load("models/best_model.pkl")
X = pd.read_csv("data/processed/X_train.csv")

print("data loaded")

# create explainer
explainer = shap.Explainer(model)

# compute shap values (sample for speed)
X_sample = X[:200]
shap_values = explainer(X_sample)

print("shap values computed")

# plot
shap.summary_plot(shap_values, X_sample, show=False)

# save plot
plt.savefig("evaluation/shap_summary.png", bbox_inches="tight")

# show plot
plt.show()

print("shap plot saved")
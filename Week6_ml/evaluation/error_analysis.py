import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.metrics import confusion_matrix

# create folder
os.makedirs("evaluation", exist_ok=True)

# load data
X = pd.read_csv("data/processed/X_train.csv")
y = pd.read_csv("data/processed/y_train.csv").values.ravel()

# load model
model = joblib.load("models/best_model.pkl")

print("model loaded")

# predictions
preds = model.predict(X)

# confusion matrix
cm = confusion_matrix(y, preds)

# plot
plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt="d")

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

# save plot
plt.savefig("evaluation/confusion_matrix.png", bbox_inches="tight")

# show plot
plt.show()

print("confusion matrix saved")
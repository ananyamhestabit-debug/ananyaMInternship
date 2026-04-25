# MODEL-COMPARISON

## 1. Introduction

In this stage, multiple machine learning models were trained and evaluated on the Titanic dataset.
The goal was to compare different algorithms and select the best-performing model.

---

## 2. Models Used

The following models were trained:

* Logistic Regression
* Random Forest
* XGBoost
* Neural Network (MLPClassifier)

Each model has a different way of learning patterns from the data.

---

## 3. Training Process

* Data was taken from the feature pipeline
* Train-test split was already applied
* Each model was trained on the same training data
* Predictions were made on test data

This ensures a fair comparison.

---

## 4. Evaluation Metrics

The models were evaluated using the following metrics:

### Accuracy

Ratio of correct predictions to total predictions.

### Precision

Out of predicted positive cases, how many were actually correct.

### Recall

Out of actual positive cases, how many were correctly identified.

### F1 Score

Balance between precision and recall.
Used as the main metric for model selection.

### ROC-AUC

Measures how well the model separates classes.

---

## 5. Model Comparison Results

Each model produced different results:

* Logistic Regression performed well on simple patterns
* Random Forest handled non-linear relationships better
* XGBoost improved performance using boosting
* Neural Network captured complex patterns in data

The evaluation results were saved in a metrics file.

---

## 6. Best Model Selection

The best model was selected based on the highest F1 score.
F1 score was chosen because it balances precision and recall.

The selected model was automatically saved for future use.

---

## 7. Observations

* Ensemble models (Random Forest, XGBoost) performed better than simple models
* Neural Network performed well but required more tuning
* Logistic Regression was fast but less flexible

---

## 8. Output Files

The following files were generated:

* models/best_model.pkl → saved best model
* evaluation/metrics.json → performance of all models

---

## 9. Conclusion

Model comparison helps identify the most suitable algorithm for the problem.
Using multiple models ensures better reliability and performance.

The selected best model is used in the next stages for tuning, explainability, and deployment.

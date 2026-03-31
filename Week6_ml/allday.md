# ML Engineering Project — Week 6 (Complete Documentation)

## Project Overview
End-to-end machine learning pipeline:
Data → EDA → Feature Engineering → Model Training → Tuning → Explainability → Deployment → Monitoring

## Environment Setup

```bash
# create virtual environment
python3 -m venv venv

# activate environment
source venv/bin/activate

# install dependencies
pip install pandas numpy seaborn matplotlib scikit-learn joblib shap fastapi uvicorn
```

---

## Project Structure

```
data/
  raw/
  processed/
notebooks/
pipelines/
features/
training/
evaluation/
deployment/
monitoring/
models/
logs/
```

---

## Day 1 — Data Pipeline + EDA

### Run Data Pipeline

```bash
python3 pipelines/data_pipeline.py
```

### Run EDA

```bash
cd notebooks
jupyter notebook
```

### python kernel: isntall and register:
-> python3 -m ipykernel install --user --name=venv --display-name "Python (venv)"

## register->
->python3 -m ipykernel install --user --name=venv --display-name "Python (venv)"

### Work Done

* Loaded raw dataset
* Removed duplicates
* Handled missing values (Age, Fare, Embarked)
* Saved cleaned dataset → `data/processed/final.csv`

### EDA

* Missing values heatmap
* Target distribution
* Feature distributions
* Correlation matrix
* Categorical analysis (Sex, Pclass)

### Observations

* Dataset slightly imbalanced
* Females survived more
* Higher class passengers survived more
* Data ready for feature engineering

## Day 2 — Feature Engineering + Selection

### Run Feature Engineering

```bash
python3 features/build_features.py
```

### Run Feature Selection

```bash
python3 features/feature_selector.py
```

### Features Created

* FamilySize
* IsAlone
* FarePerPerson
* AgeGroup
* Title
* Deck
* TicketLength
* LogFare
* AgeClass
* FareClass

### Techniques Used

* Label Encoding
* OneHot Encoding
* StandardScaler
* Train-Test Split
* Correlation Filtering
* Mutual Information
* RFE

### Outputs

```
data/processed/X_train.csv
data/processed/X_test.csv
data/processed/y_train.csv
data/processed/y_test.csv
features/feature_list.json
```

## Day 3 — Model Training

### Run Training

```bash
python3 training/train.py
```

### Models Used

* Logistic Regression
* Random Forest
* Neural Network

### Techniques

* 5-Fold Cross Validation
* Model comparison using F1 score

### Metrics

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix

### Outputs

```
models/best_model.pkl
evaluation/metrics.json
```

### Result

* Random Forest selected as best model


## Day 4 — Tuning + Explainability + Error Analysis

### Run Tuning

```bash
python3 training/tuning.py
```

### Run SHAP Analysis

```bash
python3 evaluation/shap_analysis.py
```

### Run Error Analysis

```bash
python3 evaluation/error_analysis.py
```

### Techniques

* GridSearchCV
* SHAP (feature importance)
* Confusion matrix

### Outputs

```
tuning/results.json
evaluation/shap_summary.png
evaluation/confusion_matrix.png
```

### Observations

* Model improved after tuning
* Feature importance identified using SHAP
* Errors visualized using confusion matrix


## Day 5 — Deployment + Monitoring

### Run API

```bash
uvicorn deployment.api:app --reload
```

### Open API Docs

```
http://127.0.0.1:8000/docs
```

### Sample Request

```json
{
  "Pclass": 3,
  "Sex": 1,
  "Age": 25,
  "SibSp": 0,
  "Parch": 0,
  "Fare": 7.25
}
```

### Features Implemented

* FastAPI deployment
* /predict endpoint
* Input validation (Pydantic)
* Feature engineering inside API
* Request ID tracking
* Logging with timestamp

### Logs

```bash
cat logs/prediction_logs.csv
```

### Monitoring

```bash
python3 monitoring/drift_checker.py
```

### Docker Deployment

```bash
docker build -t ml-api .
docker run -p 8000:8000 ml-api
```

## Full Project Run (All Steps)

```bash
python3 pipelines/data_pipeline.py
python3 features/build_features.py
python3 features/feature_selector.py
python3 training/train.py
python3 training/tuning.py
python3 evaluation/shap_analysis.py
python3 evaluation/error_analysis.py
uvicorn deployment.api:app --reload
```

---

## Final Summary

* Built complete ML pipeline
* Engineered and selected features
* Trained and compared models
* Tuned model performance
* Explained model using SHAP
* Deployed model using FastAPI
* Logged predictions for monitoring
* Implemented drift detection




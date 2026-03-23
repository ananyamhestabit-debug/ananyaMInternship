# Model Interpretation Report
## Best Model

The Neural Network achieved the best performance among all trained models based on evaluation metrics such as accuracy, precision, recall, F1 score, and ROC-AUC.


## Hyperparameter Tuning

RandomForest model was optimized using Optuna for better performance.

**Best Parameters:**
- n_estimators: 77  
- max_depth: 8  
- min_samples_split: 2  


## Explainability

Neural Networks are difficult to interpret directly.  
Therefore, RandomForest was used for model explainability.

The following techniques were applied:
- SHAP (SHapley Additive exPlanations)
- Feature Importance


## Key Insights

- **Fare** is one of the most influential features in predicting survival.
- **Sex (female)** has a strong positive impact on survival prediction.
- Engineered features like `Fare_log`, `Fare_squared`, and interaction features improved model performance.
- Feature engineering significantly helped in capturing hidden patterns.


## Error Analysis

- Confusion matrix was used to analyze prediction errors.
- The model shows balanced performance with minimal misclassification.
- Both false positives and false negatives are relatively low.



## Conclusion

- Neural Network is used as the final model for prediction due to its superior performance.
- RandomForest is used for interpretation and explainability.
- The pipeline successfully combines performance and interpretability.



## Final Outcome

- Best model selected  
- Hyperparameter tuning applied  
- Model explainability achieved  
- Error analysis completed  


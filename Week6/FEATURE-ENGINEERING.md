# Feature Engineering Report

## Objective

The goal of feature engineering is to create useful features to improve model performance.

---

## New Features Created

### Mathematical Features

- Fare_log: log of Fare
- Fare_squared: square of Fare
- Age_log: log of Age
- Age_squared: square of Age

---

### Interaction Features

- Pclass_Fare: Pclass multiplied by Fare
- Age_Fare_product: Age multiplied by Fare

---

### Ratio Features

- Fare_per_person: Fare divided by number of people

---

## Categorical Encoding

- One-hot encoding was applied to categorical variables such as:
  - Sex
  - Embarked

---

## Data Transformation

- Numerical features were scaled using StandardScaler.
- Categorical features were converted to numeric form.

---

## Feature Selection

Feature selection was done using:

### Correlation Filtering
- Removed highly correlated features

### Mutual Information
- Selected important features based on relation with target

### RFE
- Selected final features

---

## Final Selected Features

Examples:
- Fare
- Sex_female
- Fare_log
- Fare_squared
- Age_log
- Age_squared
- Pclass_Fare
- Age_Fare_product
- Fare_per_person

---

## Impact

- Improved model performance
- Reduced unnecessary features
- Helped capture better patterns

---

## Conclusion

Feature engineering improved the model by creating better features and removing less useful ones.
# FEATURE-ENGINEERING-DOC

## 1. Introduction

Feature engineering is the process of transforming raw data into meaningful inputs for a machine learning model.
The goal is to improve model performance by creating better features from existing data.

---

## 2. Dataset Used

The project uses the Titanic dataset.
The target variable is **Survived** (0 = not survived, 1 = survived).
Input features include:

* Pclass
* Sex
* Age
* Fare

---

## 3. Data Preparation

Before feature engineering, basic cleaning was performed:

* Missing values in Age and Fare were filled using median
* Irrelevant columns were removed
* Categorical variables were converted to numerical format

---

## 4. Feature Engineering Techniques

### 4.1 Encoding Categorical Variables

The column **Sex** is categorical (male/female).
It was converted into numeric form using one-hot encoding:

* Sex_male
* Sex_female

This allows the model to process categorical data.

---

### 4.2 Feature Transformation

#### Fare Transformation

The Fare column is highly skewed.
To reduce skewness:

* Log transformation was applied
* Square root transformation was applied

This helps stabilize variance and improves model learning.

---

#### Age Transformation

Age was also transformed to capture non-linear patterns:

* Age_squared (Age × Age)
* Age_log (log of Age)

This allows the model to learn complex relationships.

---

### 4.3 Interaction Features

New features were created by combining existing ones:

* Fare_per_person = Fare divided by number of people
* Age_Fare_product = Age × Fare
* Pclass_Fare = interaction between class and fare

These features help the model understand relationships between variables.

---

## 5. Feature Scaling

All numerical features were scaled using StandardScaler.

Formula:
z = (x - mean) / standard deviation

Scaling ensures that all features are on a similar range and no feature dominates due to large values.

---

## 6. Feature Selection

After creating features, only the most important ones were selected.
Selection was based on:

* Statistical relevance
* Contribution to model performance

The final selected features were saved in a file for reuse.

---

## 7. Output of Feature Pipeline

The feature pipeline produces:

* X_train (training features)
* X_test (testing features)
* y_train (training labels)
* y_test (testing labels)

These are used in model training.

---

## 8. Conclusion

Feature engineering improved the quality of input data by:

* Converting categorical data into numeric form
* Reducing skewness
* Creating new meaningful features
* Scaling data for better model performance

This step is essential for building an effective machine learning model.

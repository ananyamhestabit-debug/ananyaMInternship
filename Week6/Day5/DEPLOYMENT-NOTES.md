# DEPLOYMENT-NOTES

## 1. Introduction

This stage focuses on deploying the trained machine learning model so it can be used in real-world applications.
The model is exposed through an API that accepts input data and returns predictions.

---

## 2. Deployment Approach

The model is deployed using FastAPI, which is a lightweight Python framework for building APIs.
The API allows external systems (frontend, tools, or users) to interact with the model.

---

## 3. API Structure

### Endpoint

POST /predict

### Input Format (JSON)

The API expects input in JSON format:

{
"Age": value,
"Fare": value
}

### Output Format

The API returns a prediction:

{
"prediction": 0 or 1
}

---

## 4. Model Loading

The trained model is saved as a file using joblib.
During API startup, the model is loaded into memory so it can be used for predictions.

---

## 5. Input Validation

Input data is validated using Pydantic.

* Ensures correct data types (float, integer, etc.)
* Prevents invalid or missing input
* Improves reliability of the API

---

## 6. Prediction Flow

1. User sends request to /predict
2. API receives input data
3. Input is validated
4. Data is converted into model format
5. Model generates prediction
6. API returns response

---

## 7. Running the API

Command to start the server:

uvicorn deployment.api:app --reload

After running:

* API is available at http://127.0.0.1:8000
* Interactive documentation available at /docs

---

## 8. Testing the API

The API can be tested using:

* FastAPI Swagger UI (/docs)
* Postman
* curl commands

---

## 9. Docker Support

The project includes a Dockerfile to containerize the application.

Benefits:

* Same environment across systems
* Easy deployment
* No dependency conflicts

Basic steps:

1. Build image
   docker build -t ml-api .

2. Run container
   docker run -p 8000:8000 ml-api

---

## 10. Monitoring

Basic monitoring is included:

* Prediction logging (saved to CSV)
* Structure for:

  * Data drift detection
  * Model performance tracking

This helps track model behavior over time.

---

## 11. Limitations

* Model uses limited features (Age, Fare, etc.)
* No real-time retraining
* Monitoring is basic (can be improved)

---

## 12. Future Improvements

* Add more features to API input
* Improve monitoring system
* Add authentication for API
* Deploy on cloud (AWS, GCP, etc.)

---

## 13. Conclusion

Deployment makes the model usable in real-world scenarios.
The FastAPI-based system provides a simple and scalable way to serve predictions.

This completes the end-to-end ML pipeline from data to production.

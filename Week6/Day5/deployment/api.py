from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import uuid
import os
import json
import datetime

app = FastAPI()

# load model
model = joblib.load("models/best_model.pkl")

# load feature list
with open("features/feature_list.json") as f:
    feature_list = json.load(f)

# create logs folder
os.makedirs("logs", exist_ok=True)

LOG_FILE = "/app/logs/prediction_logs.csv"

# create log file
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("request_id,timestamp,input,prediction\n")


# input schema
class InputData(BaseModel):
    Pclass: int
    Sex: int
    Age: float
    SibSp: int
    Parch: int
    Fare: float


# feature engineering (same as training)
def process_input(data):
    df = pd.DataFrame([data])

    # feature engineering
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
    df["FarePerPerson"] = df["Fare"] / df["FamilySize"]

    df["LogFare"] = df["Fare"].apply(lambda x: 0 if x == 0 else x)
    df["AgeClass"] = df["Age"] * df["Pclass"]
    df["FareClass"] = df["Fare"] * df["Pclass"]

    # ensure all required features exist
    for col in feature_list:
        if col not in df.columns:
            df[col] = 0

    # reorder columns
    df = df[feature_list]

    return df


# prediction endpoint
@app.post("/predict")
def predict(input_data: InputData):
    request_id = str(uuid.uuid4())

    # convert input to dict
    input_dict = input_data.dict()

    # process features
    df = process_input(input_dict)

    # prediction
    pred = model.predict(df)[0]

    # logging
    with open(LOG_FILE, "a") as f:
        f.write(
            f"{request_id},"
            f"{datetime.datetime.now()},"
            f"{json.dumps(input_dict)},"
            f"{pred}\n"
        )

    return {
        "request_id": request_id,
        "prediction": int(pred)
    }
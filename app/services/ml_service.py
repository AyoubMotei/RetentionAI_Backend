import joblib
import pandas as pd

model = joblib.load("ml_model/retention_model_finalone.pkl")

# def predict_probability(data):

#     df =  pd.DataFrame([data.dict()])
    
#     return model.predict_proba(df)[0][1]

def predict_probability(data):
    input_data = data.dict()
    if "EmployeeId" in input_data:
        del input_data["EmployeeId"]
    df = pd.DataFrame([input_data])
    return model.predict_proba(df)[0][1]
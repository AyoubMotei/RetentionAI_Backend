import joblib
import pandas as pd

model = joblib.load("ml_model/retention_model_finalone.pkl")

def predict_probability(data):

    df =  pd.DataFrame([data.dict()])
    
    return model.predict_proba(df)[0][1]

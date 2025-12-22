from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db 
 
from .schemas import UserCreate,UserLogin,UserResponse,EmployeeFeatures,PredictionOutput,RetentionPlanOutput,RetentionPlanRequest


from app.auth import create_access_token, hash_password, verify_password, get_current_user

import joblib
from app.services.ml_service import predict_probability
from app.services.ai_services import generate_retention_plan


from dotenv import load_dotenv
import os

load_dotenv()





from app.models import User, PredictionHistory
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="RetentionAI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API opérationnelle"}



@app.post("/register")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.username == user.username).first()
    
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")
    

    hashed_pwd = hash_password(user.password)
    
    
    new_user = User(username=user.username, password_hash=hashed_pwd)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Identifiants incorrects")

    token = create_access_token(data={"sub":db_user.username})

    return {"access_token": token, "token_type": "bearer"}


@app.post("/predict", response_model=PredictionOutput)
def predict(data: EmployeeFeatures, user: dict=Depends(get_current_user)):

    proba = predict_probability(data)


    return {"churn_probability": float(proba)}

        


@app.post(
    "/retention-plan",
    response_model=RetentionPlanOutput,
    # summary="Generate Retention Plan Endpoint"
)

def generate_retention_plan_endpoint(
    employee: EmployeeFeatures,
    current_user=Depends(get_current_user)
):
    
    probability = float(predict_probability(employee))

    
    employee_data = employee.dict()

    actions = generate_retention_plan(probability, employee_data)

    if actions is None:
        return {
           
            "retention_plan": ["Risque faible — aucune action de rétention requise",]
            
        }

    return {
       
        "retention_plan": actions
    }

@app.get("/test-env")
def test_env():
    return {
        "Gemini_key_configured": bool(os.getenv("GEMINI_API_KEY")),
        "jwt_secret_configured": bool(os.getenv("JWT_SECRET_KEY")),
        "Gemini_key_preview": os.getenv("GEMINI_API_KEY", "")[:10] + "..." if os.getenv("GEMINI_API_KEY") else "None"
    }
    
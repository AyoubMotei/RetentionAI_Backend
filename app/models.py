from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from app.database import Base
from datetime import datetime



class User(Base):
    __tablename__ = "users"
    
    
    id = Column(Integer, primary_key=True, index=True)
   
    username = Column(String(50), unique=True, nullable=False)
    
    password_hash = Column(String(255), nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    



class PredictionHistory(Base):
    __tablename__="prediction_history"
    
    id = Column(Integer, primary_key=True, index=True)
    
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    
    employee_id = Column(String, nullable=False )
    
    probability = Column(String)
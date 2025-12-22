from pydantic import BaseModel
from typing import List, Optional

# Schémas Utilisateur

class UserCreate(BaseModel):
    username: str 
    password: str  

class UserLogin(UserCreate):
    pass 


class UserResponse(UserCreate):
    id : int
    
    


class EmployeeFeatures(BaseModel):
    Age: int
    BusinessTravel: str
    DailyRate: int
    Department: str
    DistanceFromHome: int
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    HourlyRate: int
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: int
    MonthlyRate: int
    NumCompaniesWorked: int
    OverTime: str
    PercentSalaryHike: int
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int
    YearsWithCurrManager: int


class PredictionOutput(BaseModel):
    churn_probability: float
    # prediction: str
    
# class RetentionPlanOutput(BaseModel):
#     retention_plan: list
    
class RetentionPlanOutput(BaseModel):
    
    retention_plan: List[str]
   
    
class RetentionPlanRequest(BaseModel):
    Age: int
    Department: str
    JobRole: str
    JobSatisfaction: int
    WorkLifeBalance: int
    PerformanceRating: int
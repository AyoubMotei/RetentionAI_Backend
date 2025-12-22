import pytest
from app.services.ml_service import predict_probability
from app.schemas import EmployeeFeatures


def test_predict_probability_returns_probability():
    employee = EmployeeFeatures.model_construct(
        
        # NUMÉRIQUES (utilisées par le modèle)
        Age=45,
        DailyRate=1100,
        DistanceFromHome=5,
        Education=4,
        EnvironmentSatisfaction=4,
        HourlyRate=95,
        JobInvolvement=4,
        JobLevel=4,
        JobSatisfaction=4,
        MonthlyIncome=14000,
        MonthlyRate=21000,
        NumCompaniesWorked=1,
        PercentSalaryHike=15,
        PerformanceRating=4,
        RelationshipSatisfaction=4,
        StockOptionLevel=3,
        TotalWorkingYears=22,
        TrainingTimesLastYear=4,
        WorkLifeBalance=4,
        YearsAtCompany=15,
        YearsInCurrentRole=10,
        YearsSinceLastPromotion=2,
        YearsWithCurrManager=8,

        #CATÉGORIELLES (REQUIS PAR LE PIPELINE)
        BusinessTravel="Non-Travel",
        Department="Research & Development",
        EducationField="Life Sciences",
        Gender="Male",
        JobRole="Research Director",
        MaritalStatus="Married",
        OverTime="No",
    )

    probability = predict_probability(employee)

    assert isinstance(probability, float)
    assert 0.0 <= probability <= 1.0

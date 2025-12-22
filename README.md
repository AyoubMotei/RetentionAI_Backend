#  RetentionAI Backend

## Vue d'ensemble

**RetentionAI Backend** est une API REST développée avec **FastAPI** qui combine Machine Learning supervisé et Intelligence Artificielle générative pour prédire les risques de départ d'employés et générer des plans de rétention personnalisés.

### Fonctionnalités Principales

- **Authentification JWT** sécurisée avec hachage Argon2
- **Prédiction ML** : Probabilité de départ via Random Forest/Régression Logistique
- **IA Générative** : Plans de rétention via Google Gemini AI
- **Base PostgreSQL** : Persistance des utilisateurs et historique des prédictions
- **Tests unitaires** avec Pytest et mocks
- **Traçabilité** : Historique complet des prédictions par utilisateur

---

## Technologies Utilisées

| Technologie | Version | Usage |
|------------|---------|-------|
| **Python** | 3.11+ | Langage principal |
| **FastAPI** | 0.100.0 | Framework web moderne |
| **SQLAlchemy** | 2.0.0 | ORM pour PostgreSQL |
| **PostgreSQL** | 15+ | Base de données relationnelle |
| **Pydantic** | 2.0.0 | Validation de données |
| **python-jose** | 3.3.0 | Gestion JWT |
| **passlib** | 1.7.4 | Hachage Argon2 |
| **scikit-learn** | 1.3.0 | Modèle ML (via joblib) |
| **Google Generative AI** | 0.3.0 | Gemini API |
| **Pytest** | 7.4.0 | Tests unitaires |
| **python-dotenv** | 1.0.0 | Gestion variables d'environnement |
| **Uvicorn** | 0.23.0 | Serveur ASGI |

---

##  Architecture du Projet

### Architecture Technique

```
┌─────────────────────────────────────────────────────┐
│              CLIENT (Frontend Next.js)              │
└─────────────────────────────────────────────────────┘
                        ↓ HTTP/REST
┌─────────────────────────────────────────────────────┐
│           FASTAPI APPLICATION (Port 8000)           │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │           MAIN.PY (Endpoints)                │  │
│  │  • /register  • /login  • /predict           │  │
│  │  • /retention-plan  • /health                │  │
│  └──────────────────────────────────────────────┘  │
│                        ↓                            │
│  ┌──────────────────────────────────────────────┐  │
│  │         AUTH.PY (JWT + Argon2)               │  │
│  └──────────────────────────────────────────────┘  │
│                        ↓                            │
│  ┌──────────────────────────────────────────────┐  │
│  │       SERVICES/                              │  │
│  │  • ml_service.py  → Modèle .pkl              │  │
│  │  • ai_services.py → Gemini API               │  │
│  └──────────────────────────────────────────────┘  │
│                        ↓                            │
│  ┌──────────────────────────────────────────────┐  │
│  │         DATABASE.PY (SQLAlchemy)             │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE                    │
│  • users  • prediction_history                      │
└─────────────────────────────────────────────────────┘
```

### Flux de Prédiction Complet

```
1. User Login → JWT Token
2. POST /predict → ML Model → Probability
3. Store in prediction_history
4. If probability > 50% → POST /retention-plan
5. Gemini API → 3 Actions personnalisées
6. Return to Frontend
```

---

##  Prérequis

Avant de commencer, assurez-vous d'avoir :

- **Python** : Version 3.11 ou supérieure
- **PostgreSQL** : Version 15 ou supérieure
- **pip** : Gestionnaire de paquets Python
- **Clé API Gemini** : Obtenir sur [Google AI Studio](https://ai.google.dev/)

Vérification :
```bash
python --version  # Python 3.11.x
psql --version    # PostgreSQL 15.x
pip --version     # pip 23.x
```

---

##  Installation

### 1. Cloner le Répertoire

```bash
git clone https://github.com/AyoubMotei/RetentionAI_Backend.git
cd RetentionAI_Backend
```

### 2. Créer un Environnement Virtuel

```bash
# Créer l'environnement
python -m venv venv

# Activer l'environnement
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Installer les Dépendances

```bash
pip install -r requirements.txt
```

**Contenu de `requirements.txt`** :
```txt
fastapi==0.100.0
uvicorn[standard]==0.23.0
sqlalchemy==2.0.19
psycopg2-binary==2.9.7
pydantic==2.1.1
python-jose[cryptography]==3.3.0
passlib[argon2]==1.7.4
python-dotenv==1.0.0
google-generativeai==0.3.1
pandas==2.0.3
scikit-learn==1.3.0
joblib==1.3.2
pytest==7.4.0
pytest-mock==3.11.1
```

### 4. Créer la Base de Données PostgreSQL

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Créer la base de données
CREATE DATABASE retentionai_db;

# Quitter
\q
```

---

## Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet :

```env
# Configuration PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=votre_mot_de_passe
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=retentionai_db

# Clé API Gemini
GEMINI_API_KEY=votre_cle_api_gemini

# Sécurité JWT
JWT_SECRET_KEY=votre_cle_secrete_tres_longue_et_aleatoire_minimum_32_caracteres
JWT_ALGORITHM=HS256
```


##  Structure des Dossiers

```
RetentionAI_Backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py                  # Point d'entrée FastAPI
│   ├── models.py                # Modèles SQLAlchemy
│   ├── schemas.py               # Schémas Pydantic
│   ├── database.py              # Configuration DB
│   ├── auth.py                  # JWT + Argon2
│   │
│   └── services/
│       ├── __init__.py
│       ├── ml_service.py        # Service ML
│       └── ai_services.py       # Service Gemini
│
├── ml_model/
│   └── retention_model_finalone.pkl  # Modèle entraîné
│
├── data/
│   └── data.csv                 # Dataset 
│
├── notebook/
│   └── data_science.ipynb       # Jupyter notebook ML
│
├── tests/
│   ├── __init__.py
│   ├── test_ml_service.py       # Tests ML
│   └── test_mock_ai_service.py  # Tests IA avec mocks
│
├── .env                         # Variables d'environnement
├── .gitignore
├── requirements.txt
├── pytest.ini
├── Dockerfile                   # Image Docker
├── docker-compose.yml           # Orchestration
└── README.md                    # Ce fichier
```

---

## Modèles de Données

### Fichier : `app/models.py`

#### 1. Modèle User

```python
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

**Description** : Stocke les utilisateurs RH avec mots de passe hachés (Argon2).

**Champs** :
- `id` : Clé primaire auto-incrémentée
- `username` : Identifiant unique (max 50 caractères)
- `password_hash` : Mot de passe haché avec Argon2
- `created_at` : Date de création du compte

---

#### 2. Modèle PredictionHistory

```python
class PredictionHistory(Base):
    __tablename__ = "prediction_history"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    employee_id = Column(String, nullable=False)
    probability = Column(String)
```

**Description** : Traçabilité des prédictions effectuées par chaque utilisateur.

**Champs** :
- `id` : Clé primaire
- `timestamp` : Date/heure de la prédiction
- `user_id` : Clé étrangère vers `users.id`
- `employee_id` : ID de l'employé analysé
- `probability` : Probabilité de départ (stockée en string)

**Relation** :
```
User (1) ──── (N) PredictionHistory
```

---

## Schémas Pydantic

### Fichier : `app/schemas.py`

#### 1. Schémas Utilisateur

```python
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(UserCreate):
    pass

class UserResponse(UserCreate):
    id: int
```

**Usage** :
- `UserCreate` : Inscription
- `UserLogin` : Connexion
- `UserResponse` : Retour après création

---

#### 2. Schéma EmployeeFeatures

```python
class EmployeeFeatures(BaseModel):
    EmployeeId: str
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
```

**Description** : 30+ variables RH pour la prédiction ML.

**Catégories** :
- **Démographiques** : Age, Gender, MaritalStatus
- **Poste** : Department, JobRole, JobLevel
- **Satisfaction** : JobSatisfaction, WorkLifeBalance, EnvironmentSatisfaction
- **Performance** : PerformanceRating, JobInvolvement
- **Rémunération** : MonthlyIncome, HourlyRate, StockOptionLevel
- **Expérience** : YearsAtCompany, TotalWorkingYears, YearsSinceLastPromotion

---

#### 3. Schémas de Sortie

```python
class PredictionOutput(BaseModel):
    churn_probability: float

class RetentionPlanOutput(BaseModel):
    retention_plan: List[str]
```

---

##  Endpoints API

### Fichier : `app/main.py`

### 1. Health Check

```http
GET /health
```

**Description** : Vérifier que l'API est opérationnelle.

**Réponse** :
```json
{
  "status": "ok",
  "message": "API opérationnelle"
}
```

**Code HTTP** : 200 OK

---

### 2. Inscription

```http
POST /register
Content-Type: application/json

{
  "username": "hr_manager",
  "password": "securepassword123"
}
```

**Traitement** :
1. Vérification si username existe déjà
2. Hachage du mot de passe avec Argon2
3. Création de l'utilisateur en base
4. Retour de l'utilisateur créé

**Réponse Succès** (201) :
```json
{
  "id": 1,
  "username": "hr_manager",
  "created_at": "2024-12-22T10:30:00"
}
```

**Erreur** (400) :
```json
{
  "detail": "Nom d'utilisateur déjà pris"
}
```

---

### 3. Connexion

```http
POST /login
Content-Type: application/json

{
  "username": "hr_manager",
  "password": "securepassword123"
}
```

**Traitement** :
1. Recherche de l'utilisateur
2. Vérification du mot de passe haché
3. Génération d'un JWT token
4. Retour du token

**Réponse Succès** (200) :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Erreur** (401) :
```json
{
  "detail": "Identifiants incorrects"
}
```

---

### 4. Prédiction ML

```http
POST /predict
Authorization: Bearer <token>
Content-Type: application/json

{
  "EmployeeId": "EMP001",
  "Age": 35,
  "Department": "Sales",
  "JobRole": "Sales Executive",
  "JobSatisfaction": 2,
  "WorkLifeBalance": 2,
  ...
}
```

**Traitement** :
1. Validation du JWT token
2. Suppression de `EmployeeId` des features
3. Prédiction avec le modèle ML (.pkl)
4. Enregistrement dans `prediction_history`
5. Retour de la probabilité

**Réponse Succès** (200) :
```json
{
  "churn_probability": 0.78
}
```

**Erreur** (401) :
```json
{
  "detail": "Token invalide ou expiré"
}
```

**Implémentation** :
```python
@app.post("/predict", response_model=PredictionOutput)
def predict(
    data: EmployeeFeatures, 
    user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    proba = predict_probability(data)
    
    current_user = db.query(User).filter(User.username == user).first()
    
    if current_user:
        history_entry = PredictionHistory(
            user_id=current_user.id,
            employee_id=data.EmployeeId,
            probability=str(proba)
        )
        db.add(history_entry)
        db.commit()
    
    return {"churn_probability": float(proba)}
```

---

### 5. Génération Plan de Rétention

```http
POST /retention-plan
Authorization: Bearer <token>
Content-Type: application/json

{
  "EmployeeId": "EMP001",
  "Age": 35,
  "Department": "Sales",
  ...
}
```

**Traitement** :
1. Validation du JWT token
2. Prédiction de la probabilité
3. Si probabilité ≤ 50% → Message "Risque faible"
4. Si probabilité > 50% → Appel Gemini API
5. Parsing des 3 actions générées
6. Retour du plan

**Réponse Succès (Risque Élevé)** (200) :
```json
{
  "retention_plan": [
    "Proposer 2 jours de télétravail par semaine",
    "Réévaluer la charge de déplacement professionnel",
    "Plan de formation personnalisé en leadership"
  ]
}
```

**Réponse (Risque Faible)** (200) :
```json
{
  "retention_plan": [
    "Risque faible — aucune action de rétention requise"
  ]
}
```

**Implémentation** :
```python
@app.post("/retention-plan", response_model=RetentionPlanOutput)
def generate_retention_plan_endpoint(
    employee: EmployeeFeatures,
    current_user=Depends(get_current_user)
):
    probability = float(predict_probability(employee))
    employee_data = employee.dict()
    
    actions = generate_retention_plan(probability, employee_data)
    
    if actions is None:
        return {
            "retention_plan": ["Risque faible — aucune action de rétention requise"]
        }
    
    return {"retention_plan": actions}
```

---

##  Authentification JWT

### Fichier : `app/auth.py`

### Hachage des Mots de Passe (Argon2)

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

---

### Gestion JWT

#### Création d'un Token

```python
from jose import jwt

def create_access_token(data: dict) :
    to_encode = data.copy()
    encoded_jwt = jwt.encode(
        to_encode, 
        JWT_SECRET_KEY, 
        algorithm=JWT_ALGORITHM
    )
    return encoded_jwt
```

**Payload JWT** :
```json
{
  "sub": "hr_manager"
}
```

---

#### Décodage d'un Token

```python
def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            JWT_SECRET_KEY, 
            algorithms=[JWT_ALGORITHM]
        )
        if not payload.get("sub"):
            raise JWTError("sub manquant")
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token invalide ou expiré",
            headers={"WWW-Authenticate": "Bearer"}
        )
```

---

#### Extraction du Token (Dependency)

```python
from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()

async def get_current_user(
    creds: HTTPBasicCredentials = Depends(bearer_scheme)
):
    token = creds.credentials
    payload = decode_access_token(token)
    return payload.get("sub")  # Retourne le username
```

**Usage dans un endpoint** :
```python
@app.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Bonjour {current_user}"}
```

---

## Service Machine Learning

### Fichier : `app/services/ml_service.py`

```python
import joblib
import pandas as pd

model = joblib.load("ml_model/retention_model_finalone.pkl")

def predict_probability(data: EmployeeFeatures) :
    input_data = data.dict()
    
    # Supprimer EmployeeId (non utilisé par le modèle)
    if "EmployeeId" in input_data:
        del input_data["EmployeeId"]
    
    df = pd.DataFrame([input_data])
    
    # Prédiction de la probabilité de la classe 1 (départ)
    return model.predict_proba(df)[0][1]
```

### Détails Techniques

**Modèle Utilisé** :
- Type : Random Forest Classifier / Régression Logistique
- Format : `.pkl` (via joblib)
- Features : 30 variables (numériques + catégorielles)
- Sortie : Probabilité entre 0 et 1

**Pipeline Intégré** :
Le modèle `.pkl` contient un pipeline complet :
1. **OneHotEncoder** : Encodage des variables catégorielles
2. **StandardScaler** : Normalisation des variables numériques
3. **Classifier** : Random Forest ou Régression Logistique

**Variables Catégorielles Encodées** :
- BusinessTravel
- Department
- EducationField
- Gender
- JobRole
- MaritalStatus
- OverTime

---

### Exemple de Prédiction

**Input** :
```python
employee = EmployeeFeatures(
    EmployeeId="EMP001",
    Age=35,
    Department="Sales",
    JobSatisfaction=2,
    ...
)
```

**Output** :
```python
probability = predict_probability(employee)
# 0.78 (78% de risque de départ)
```

---

##  Service IA Générative

### Fichier : `app/services/ai_services.py`

```python
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def generate_retention_plan(probability: float, employee: dict):
    if probability <= 0.50:
        return None
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        response = model.generate_content(
            build_prompt(probability, employee)
        )
        
        # Parsing des actions
        actions = []
        for line in response.text.splitlines():
            if line.lower().startswith("action"):
                actions.append(line.split(":", 1)[1].strip())
        
        return actions[:3]
    
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return [
            "Service IA indisponible",
            "Veuillez réessayer ultérieurement"
        ]
```

---

### Prompt Engineering

```python
def build_prompt(probability: float, employee: dict):
    return f"""
Agis comme un expert RH senior.

Employé :
- Âge : {employee["Age"]}
- Département : {employee["Department"]}
- Rôle : {employee["JobRole"]}
- Satisfaction au travail : {employee["JobSatisfaction"]}
- Équilibre vie pro / perso : {employee["WorkLifeBalance"]}
- Performance : {employee["PerformanceRating"]}

Contexte :
Cet employé présente un risque élevé de départ volontaire ({probability:.0%}).

Tâche :
Propose EXACTEMENT 3 actions concrètes, personnalisées et immédiatement applicables
pour retenir cet employé.

Format STRICT attendu :
Action 1 : ...
Action 2 : ...
Action 3 : ...

Contraintes :
- Français professionnel
- Pas de généralités
- Pas de markdown
"""
```

### Stratégie de Prompt

**Éléments Clés** :
1. **Rôle** : "Expert RH senior" → Guide le ton et l'expertise
2. **Contexte** : Données employé + probabilité → Personnalisation
3. **Tâche** : "EXACTEMENT 3 actions" → Contrainte stricte
4. **Format** : "Action 1 :", "Action 2 :" → Parsing facile
5. **Contraintes** : Éviter généralités et markdown → Qualité

---

### Exemple de Réponse Gemini

**Input** :
```
Probabilité : 78%
Âge : 35
Département : Sales
JobSatisfaction : 2/4
```

**Output** :
```
Action 1 : Proposer 2 jours de télétravail par semaine pour améliorer l'équilibre vie pro/perso
Action 2 : Réévaluer la charge de déplacement professionnel qui impacte la satisfaction
Action 3 : Mettre en place un plan de formation personnalisé en leadership pour valoriser ses compétences
```

---

##  Base de Données

### Fichier : `app/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = f'postgresql+psycopg2://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DB")}'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

### Connexion PostgreSQL

**URL Format** :
```
postgresql+psycopg2://user:password@host:port/database
```

**Exemple** :
```
postgresql+psycopg2://postgres:123@localhost:5432/retentionai_db
```

---

### Création Automatique des Tables

Dans `main.py` :
```python
from app.models import User, PredictionHistory
from app.database import Base, engine

Base.metadata.create_all(bind=engine)
```

Cette ligne crée automatiquement les tables `users` et `prediction_history` au démarrage si elles n'existent pas.

---

### Dependency Injection

```python
@app.post("/predict")
def predict(
    data: EmployeeFeatures,
    db: Session = Depends(get_db)
):
    # db est une session SQLAlchemy injectée automatiquement
    user = db.query(User).filter(User.username == "test").first()
    ...
```

---

## Tests Unitaires

### Fichier : `pytest.ini`

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

---

### Test 1 : Service ML

**Fichier** : `tests/test_ml_service.py`

```python
import pytest
from app.services.ml_service import predict_probability
from app.schemas import EmployeeFeatures

def test_predict_probability_returns_probability():
    employee = EmployeeFeatures.model_construct(
        EmployeeId="TEST001",
        Age=45,
        DailyRate=1100,
        Department="Research & Development",
        JobRole="Research Director",
        JobSatisfaction=4,
        # ... toutes les autres features
    )
    
    probability = predict_probability(employee)
    
    assert isinstance(probability, float)
    assert 0.0 <= probability <= 1.0
```

**Objectif** : Vérifier que le modèle charge correctement et retourne une probabilité valide.

---

### Test 2 : Service IA avec Mock

**Fichier** : `tests/test_mock_ai_service.py`

```python
from app.services.ai_services import generate_retention_plan

def test_generate_retention_plan_with_mocked_llm():
    # Mock du modèle Gemini
    mock_model = mocker.Mock()
    mock_model.generate_content.return_value = fake_response

    mocker.patch(
        "app.services.ai_services.genai.GenerativeModel",
        return_value=mock_model
    )

    probability = 0.8
    employee = {
        "Age": 35,
        "Department": "Sales",
        "JobRole": "Sales Executive",
        "JobSatisfaction": 2,
        "WorkLifeBalance": 2,
        "PerformanceRating": 3,
    }

    actions = generate_retention_plan(probability, employee)

    assert isinstance(actions, list)
    assert len(actions) == 3

```

**Objectif** : Tester la logique sans appeler réellement l'API Gemini (limite de quota).

**Dépendance** :
```bash
pip install pytest-mock
```

---

### Lancer les Tests
```bash
# Tous les tests
pytest

# Avec verbosité
pytest -v

# Test spécifique
pytest tests/test_ml_service.py

```

---

##  Développement

### Démarrer le Serveur
```bash
# Avec reload automatique
uvicorn app.main:app --reload

# Sur un port spécifique
uvicorn app.main:app --reload --port 8000

# Accessible depuis l'extérieur
uvicorn app.main:app --reload --host 0.0.0.0
```

**L'API démarre sur** : `http://localhost:8000`

---

### Documentation Interactive

FastAPI génère automatiquement deux documentations interactives :

#### Swagger UI
http://localhost:8000/docs

---
**Dernière mise à jour** : Décembre 2025  
**Version** : 1.0.0  
**Auteur** : AYOUB MOTEI
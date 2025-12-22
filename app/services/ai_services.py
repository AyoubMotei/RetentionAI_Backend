import google.generativeai as genai
from app.schemas import RetentionPlanOutput
import os
from dotenv import load_dotenv 

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


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


Format de sortie OBLIGATOIRE :
- Une liste de 3 phrases, une par ligne


Contraintes :
- Français professionnel
- Pas de généralités
- Pas de markdown
"""


def generate_retention_plan(probability: float, employee: dict):
    if probability <= 0.50:
        return None

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(
        build_prompt(probability, employee)
    )

    # Nettoyage simple → liste
    actions = []
    for line in response.text.splitlines():
        if line.lower().startswith("action"):
            actions.append(line.split(":", 1)[1].strip())

    return actions[:3]

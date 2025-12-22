from app.services.ai_services import generate_retention_plan


def test_generate_retention_plan_with_mocked_llm(mocker):
    
    # Fake response Gemini
    fake_response = mocker.Mock()
    fake_response.text = (
        "Action 1 : Proposer 2 jours de télétravail\n"
        "Action 2 : Réduire la charge de travail temporairement\n"
        "Action 3 : Mettre en place un plan de formation personnalisé"
    )

    # Mock du modèle Gemini
    mock_model = mocker.Mock()
    mock_model.generate_content.return_value = fake_response

    # Chemain de ai_services
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

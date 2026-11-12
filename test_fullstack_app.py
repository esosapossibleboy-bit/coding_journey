from fastapi.testclient import TestClient
from mood_api import app

client = TestClient(app)

def test_fullstack_homepage_and_api():
    # Test 1: Front door "/" serves our interactive HTML app
    page = client.get("/")
    assert page.status_code == 200
    assert "Full-Stack AI Mood Analyzer" in page.text
    assert 'id="userInput"' in page.text
    assert 'fetch("/analyze?text="' in page.text

    # Test 2: Backend "/analyze" still works seamlessly
    api_res = client.get("/analyze?text=This full stack app is awesome")
    assert api_res.status_code == 200
    assert api_res.json()["mood"] == "Positive"

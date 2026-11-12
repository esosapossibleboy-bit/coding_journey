from fastapi.testclient import TestClient
from mood_api import app

client = TestClient(app)

def test_live_ai_endpoint():
    # Test 1: Send a positive message to the /analyze web URL
    response = client.get("/analyze?text=I love building APIs")
    assert response.status_code == 200
    assert response.json() == {"text": "I love building APIs", "mood": "Positive"}
    
    # Test 2: Send a negative message
    response2 = client.get("/analyze?text=This bug is bad")
    assert response2.status_code == 200
    assert response2.json() == {"text": "This bug is bad", "mood": "Negative"}

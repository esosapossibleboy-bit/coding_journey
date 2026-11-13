from fastapi.testclient import TestClient
import study_server

client = TestClient(study_server.app)

def test_study_buddy_web_dashboard():
    res = client.get("/")
    assert res.status_code == 200
    assert "Esosa's AI Study Buddy" in res.text
    assert 'id="authScreen"' in res.text
    assert 'id="appScreen"' in res.text


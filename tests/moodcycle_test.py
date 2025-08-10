import random
import string
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def enter_random_mood():
    return random.choice(['happy', 'sad', 'neutral', 'angry', 'excited', 'tired'])

def random_session_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=36))

def test_mood_cycle_and_stress():
    user_id = random_session_id()
    client.cookies.set("user_id", user_id)

    initial = client.get("/logged-moods")
    assert initial.status_code == 200
    assert "moods" in initial.json() or "message" in initial.json()


    test_mood = {"mood": "feeling good"}
    response = client.post("/mood", json=test_mood)
    assert response.status_code == 200
    assert response.json().get("message") == "Mood successfully added!"


    for _ in range(200):
        r = client.post("/mood", json={"mood": enter_random_mood()})
        assert r.status_code == 200

  
    result = client.get("/logged-moods")
    assert result.status_code == 200
    moods = result.json().get("moods", [])
    assert len(moods) == 201  # 200 random + 1 'feeling good' test

  
    assert any(m["mood"] == "feeling good" for m in moods)

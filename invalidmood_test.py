import random
import string
from fastapi.testclient import TestClient
from main import app  # tests/__init__.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


client = TestClient(app)

def random_session_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=36))

def test_invalid_mood_input():
    user_id = random_session_id()
    client.cookies.set("user_id", user_id)

    response_missing = client.post("/mood", json={})
    assert response_missing.status_code == 422  # Unprocessable Entity from FastAPI validation

   
    response_wrong_type = client.post("/mood", json={"mood": 123})
    assert response_wrong_type.status_code == 422


    response_empty = client.post("/mood", json={"mood": ""})
  
    assert response_empty.status_code in (200, 422)

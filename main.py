from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, date
import os
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'mood.history.txt')
app.mount("/static", StaticFiles(directory="static"), name="static")

class MoodEntry(BaseModel):
    mood: str


@app.post('/mood')
def log_mood(entry: MoodEntry):
    date_today = date.today()
    formatted_date = date_today.strftime("%d-%m-%Y")
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(f'{formatted_date}, {hour}:{minute}: {entry.mood}\n')

@app.get('/logged-moods')
def view_moods():
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if not lines:
                return {'moods': [], 'message': 'No moods saved yet.'}
            else:
                return {'moods': [line.strip() for line in lines]}
    except FileNotFoundError:
        return {'moods': [], 'message': "No moods saved yet.."}
    


index_path = os.path.join(script_dir, "static", "index.html")

@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open(index_path, "r", encoding="utf-8") as file:
        return file.read()














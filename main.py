import uuid
from datetime import datetime
from fastapi import FastAPI, Request, Response, Cookie
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from models import MoodEntry
from database import create_table, add_mood, delete_mood_db, get_mood_count, get_moods
from sentiment_analysis import classify_sentiment



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

create_table()

@app.middleware("http")
async def add_user_id_cookie(request: Request, call_next):
    user_id = request.cookies.get("user_id")
    if not user_id:
        user_id = str(uuid.uuid4())
    response: Response = await call_next(request)
    if "user_id" not in request.cookies:
        response.set_cookie(key="user_id", value=user_id, max_age=60*60*24*365*10)
    return response


@app.get("/", response_class=HTMLResponse)
def root():
    return FileResponse("static/index.html")


@app.post("/mood")
def log_mood(entry: MoodEntry, user_id: str = Cookie(None)):
    if not user_id:
        user_id = str(uuid.uuid4())

    mood_to_save = entry.mood.lower()
    sentiment, polarity = classify_sentiment(mood_to_save)

    now = datetime.now()
    time_str = f"{now.year}-{now.month:02d}-{now.day:02d} {now.hour}:{now.minute:02d}"

    add_mood(user_id, time_str, mood_to_save, sentiment)

    return {
        "message": "Mood successfully added!",
        "mood": mood_to_save,
        "sentiment": sentiment,
        "polarity": polarity
    }

@app.get("/logged-moods")
def show_moods(user_id: str = Cookie(None)):
    if not user_id:
        return {"moods": []} 
    moods = get_moods(user_id)
    if not moods:
        return {"moods": []}

    # Compute polarity dynamically
    moods_with_polarity = []
    for m in moods:
        _, polarity = classify_sentiment(m["mood"])
        moods_with_polarity.append({
            "mood_id": m["mood_id"],
            "time": m["time"],
            "mood": m["mood"],
            "polarity": polarity
        })

    return {"moods": moods_with_polarity}

@app.delete("/mood/delete/{mood_id}")
def delete_mood(mood_id: int):
    delete_mood_db(mood_id)
    return {"message": "Mood successfully deleted!"}

@app.get("/mood-count")
def show_mood_count(user_id: str = Cookie(None)):
    if not user_id:
        return {"message": "No user ID found in cookies."}
    count = get_mood_count(user_id)
    return {"message": f"{count} mood{'s' if count != 1 else ''} logged so far."}

Mood Tracker API
This is a simple FastAPI web app that lets you log your mood and view your mood history.

What it does
POST /mood — Accepts a mood entry (a short text like "happy" or "stressed") and saves it with the current date and time to a file (mood.history.txt).

GET /logged-moods — Reads all saved mood entries from the file and returns them as a list.

GET / — Serves the homepage (index.html) from the static folder, which can be a simple interface to interact with the API.

How it works
Moods are sent as JSON with a single field called mood.

Each mood entry is timestamped with the day, hour, and minute when it was logged.

The app stores the data in a plain text file in the same directory.

Static files like the homepage HTML and CSS live in a static folder.

If the mood file doesn't exist or is empty, the app will respond gracefully with an empty list and a message.

Why this is useful
It’s a lightweight way to track your mood over time without a database.

The app is easy to extend with more features or a nicer frontend.

It’s a practical example of how to use FastAPI with file I/O, data validation, and serving static files.

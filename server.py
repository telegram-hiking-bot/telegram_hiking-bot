from flask import Flask, request
import requests
import datetime
import pytz

app = Flask(__name__)

# Telegram Bot Token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Function to fetch calendar busy times
def get_busy_times(access_token):
    url = "https://www.googleapis.com/calendar/v3/freeBusy"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    now = datetime.datetime.now(pytz.timezone("America/Sao_Paulo"))
    time_min = now.replace(hour=6, minute=0, second=0, microsecond=0)
    time_max = now + datetime.timedelta(days=3)
    time_max = time_max.replace(hour=18, minute=0, second=0, microsecond=0)

    data = {
        "timeMin": time_min.isoformat(),
        "timeMax": time_max.isoformat(),
        "timeZone": "America/Sao_Paulo",
        "items": [{"id": "primary"}]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        busy_times = response.json()["calendars"]["primary"]["busy"]
        return busy_times
    else:
        print("Error fetching calendar:", response.text)
        return []

# Root GET route for testing
@app.route("/", methods=["GET"])
def index():
    return "Hello, this is the Hiking Bot webhook server."

# Telegram webhook route
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and data["message"].get("text"):
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].lower()

        if "availability" in text:
            # Paste your current access token below (from OAuth Playground)
            access_token = "YOUR_ACCESS_TOKEN_HERE"
            busy_times = get_busy_times(access_token)

            if busy_times:
                reply = "You're busy at these times:\n"
                for slot in busy_times:
                    start = slot["start"]
                    end = slot["end"]
                    reply += f"- {start} to {end}\n"
            else:
                reply = "You're fully available for the next 3 days between 6am and 6pm!"
        else:
            reply = f"You said: {text}"

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )
    return "OK"

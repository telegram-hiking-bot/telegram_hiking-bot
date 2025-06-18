from flask import Flask, request
import requests
import datetime
import pytz
from weather import get_weather  # ✅ NEW IMPORT

app = Flask(__name__)

# Replace with your actual Telegram bot token
BOT_TOKEN = "7975572544:AAHeTn1bCV3EGe2lIP0FOtmO8TTSJKsEPtY"

# Replace with your actual OAuth 2.0 values
CLIENT_ID = "327270170022-8ie6e374rssrgdjh3osru3u2f94trsek.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REFRESH_TOKEN = "1//04GhZEvsvunOICgYIARAAGAQSNwF-L9Irvp6-RSqWYWp7nMcNfjS6ckL8lJ8QDe1LygiepuW6CbIyIdmLz3ibENULuZoL0yTtBAo"

def get_access_token():
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print("Failed to refresh access token:", response.text)
        return None

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
        return response.json()["calendars"]["primary"]["busy"]
    else:
        print("Error fetching calendar:", response.text)
        return []

@app.route("/", methods=["GET"])
def index():
    return "Hiking Bot Webhook is running."

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and data["message"].get("text"):
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"].strip().lower()

        if "availability" in text:
            access_token = get_access_token()
            if not access_token:
                reply = "Failed to authenticate with Google Calendar."
            else:
                busy_times = get_busy_times(access_token)
                if busy_times:
                    reply = "You're busy at these times:\n"
                    for slot in busy_times:
                        reply += f"- {slot['start']} to {slot['end']}\n"
                else:
                    reply = "You're fully available for the next 3 days between 6am and 6pm!"

        elif "weather" in text:  # ✅ NEW BLOCK
            city = "São José dos Campos"
            api_key = "ae51aaa17bd3f521d112965df4761828"
            reply = get_weather(city, api_key)

        else:
            reply = f"You said: {text}"

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )

    return "OK"

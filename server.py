from flask import Flask, request
import requests

app = Flask(__name__)
BOT_TOKEN = "7975572544:AAHeTn1bCV3EGe2lIP0FOtmO8TTSJKsEPtY"

@app.route("/", methods=["GET"])
def index():
    return "Hello, this is the Hiking Bot webhook server."
import datetime
import pytz

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

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and data["message"].get("text"):
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        reply = f"You said: {text}"
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )
    return "OK"


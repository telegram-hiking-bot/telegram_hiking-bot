from flask import Flask, request
import requests

app = Flask(__name__)
BOT_TOKEN = "7975572544:AAHeTn1bCV3EGe2lIP0FOtmO8TTSJKsEPtY"

@app.route("/", methods=["GET"])
def index():
    return "Hello, this is the Hiking Bot webhook server."

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


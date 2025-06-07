from flask import Flask, request
import os
import requests

app = Flask(__name__)

UNISENDER_API_KEY = os.getenv("UNISENDER_API_KEY")
LIST_ID = os.getenv("LIST_ID")

@app.route("/", methods=["GET", "POST"])
def receive_webhook():
    email = request.args.get("email")  # берем из URL-параметров
    if not email:
        return "Ошибка: email не передан", 400

    payload = {
        "api_key": UNISENDER_API_KEY,
        "list_ids": LIST_ID,
        "fields[email]": email,
        "double_optin": 0
    }

    response = requests.post(
        "https://api.unisender.com/ru/api/subscribe?format=json",
        data=payload
    )

    if response.status_code == 200 and response.json().get("result"):
        return "OK", 200
    else:
        return f"Ошибка UniSender: {response.text}", 500

if __name__ == "__main__":
    app.run()

from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receive_webhook():
    data = request.json
    try:
        email = data["contact"]["email"][0]["value"]
    except (KeyError, IndexError):
        return "Ошибка: неверная структура JSON", 400

    UNISENDER_API_KEY = os.getenv("UNISENDER_API_KEY")
    LIST_ID = os.getenv("LIST_ID")

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
        return f"Ошибка Unisender: {response.text}", 500

if __name__ == "__main__":
    app.run()

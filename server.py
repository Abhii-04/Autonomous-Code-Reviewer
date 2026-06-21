from flask import Flask, request, jsonify
import os

app = Flask(__name__)


@app.route("/")
def home():
    return {
        "status": "running",
        "message": "Autonomous Code Reviewer API"
    }


@app.route("/health")
def health():
    return {
        "status": "healthy"
    }


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.json

    print("=" * 60)
    print("Webhook received!")
    print(payload)
    print("=" * 60)

    return jsonify({
        "success": True
    })


@app.route("/env")
def env():
    return print("hello")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

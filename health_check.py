"""
Health check endpoint for deployment
"""
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def health():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, jsonify
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route("/api/health")
def health_check():
    """Health check endpoint to verify API status."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(pytz.UTC).isoformat(),
        "version": "1.0.0"
    })

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"
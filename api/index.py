from flask import Flask, jsonify
from datetime import datetime

"""
Flask application for the Gym Bacteria Agents API
Provides health monitoring and basic endpoints for the application
"""
app = Flask(__name__)

@app.route("/api/health")
def health_check():
    """
    Health check endpoint to verify API status.
    Returns:
        JSON with current health status, timestamp, and API version
        {
            "status": str,
            "timestamp": str (ISO format),
            "version": str
        }
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "0.1.0"
    })

@app.route("/api/python")
def hello_world():
    """
    Simple test endpoint that returns a Hello World message.
    Returns:
        str: HTML string containing "Hello, World!"
    """
    return "<p>Hello, World!</p>"
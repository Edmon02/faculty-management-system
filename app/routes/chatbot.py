# app/routes/chatbot.py
import traceback

from flask import Blueprint, jsonify, render_template, request
from flask_cors import cross_origin

from app.services.thesis_service import ThesisService

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    return render_template("chatbot.html")


@chatbot_bp.route("/generate_text", methods=["POST"])
@cross_origin()
def generate_text():
    thesis_service = ThesisService()
    data = request.json
    user_message = data.get("user_message")
    chatbot = data.get("chatbot", [])
    history = data.get("history", [])

    try:
        result = thesis_service.generate_text(user_message, history, chatbot)
        return jsonify(result)
    except Exception as e:
        # If an exception occurs, capture the traceback information
        error_traceback = traceback.format_exc()
        # Create a JSON response containing the error information
        error_response = {"chatbot": str(e), "history": error_traceback}

        # Return the error response with a specific status code (e.g., 500 for internal server error)
        return jsonify(error_response), 500

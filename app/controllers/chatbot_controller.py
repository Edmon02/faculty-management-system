import traceback

from flask import jsonify, render_template, request

from app.services.chatbot_service import ChatbotService


class ChatbotController:
    @staticmethod
    def show_chatbot():
        return render_template("chatbot.html")

    @staticmethod
    def generate_text():
        data = request.json
        user_message = data.get("user_message")
        chatbot = data.get("chatbot", [])
        history = data.get("history", [])
        temperature = data.get("temperature", 0.7)
        top_p = data.get("top_p", 0.9)
        max_new_tokens = data.get("max_new_tokens", 1024)
        repetition_penalty = data.get("repetition_penalty", 1.2)

        # Format chatbot history
        formatted_chatbot = []
        for i in range(0, len(chatbot) - 1, 2):
            if i + 1 < len(chatbot) and chatbot[i]["user"] == True:
                formatted_chatbot.append((chatbot[i]["text"], chatbot[i + 1]["text"]))

        try:
            chatbot_service = ChatbotService()
            result = chatbot_service.generate(user_message, history, formatted_chatbot)
            return jsonify(result)
        except Exception as e:
            # Capture traceback information for debugging
            error_traceback = traceback.format_exc()
            error_response = {"chatbot": str(e), "history": error_traceback}
            return jsonify(error_response), 500

import base64
from datetime import datetime

from flask import current_app, flash, jsonify, redirect, render_template, request, session, url_for

from app.services.news_service import NewsService


class NewsController:
    @staticmethod
    def get_news():
        news_service = NewsService()
        is_react_frontend = request.headers.get("X-React-Frontend")

        news = news_service.get_all_news()

        if is_react_frontend:
            # Convert binary image data to base64 for API response
            for item in news:
                if "cover" in item and item["cover"]:
                    item["cover"] = base64.b64encode(item["cover"]).decode("utf-8")

            return jsonify(news)

        return render_template("index.html")

    @staticmethod
    def get_news_by_id(id):
        news_service = NewsService()
        is_react_frontend = request.headers.get("X-React-Frontend")

        news = news_service.get_news_by_id(id)

        if is_react_frontend:
            # Convert binary data to base64 for API response
            for item in news:
                # Convert cover image to base64
                if "cover" in item and item["cover"]:
                    item["cover"] = base64.b64encode(item["cover"]).decode("utf-8")

                # Convert audio to base64 if it exists
                if "audio" in item and item["audio"] and isinstance(item["audio"], bytes):
                    item["audio"] = base64.b64encode(item["audio"]).decode("utf-8")

            return jsonify(news)

        return render_template("index.html")

    @staticmethod
    def get_audio_chunk(news_id, chunk_id):
        news_service = NewsService()
        is_react_frontend = request.headers.get("X-React-Frontend")

        audio_chunk = news_service.get_audio_chunk(news_id, chunk_id)

        if is_react_frontend:
            # Convert audio data to base64
            for item in audio_chunk:
                if "audio_data" in item and item["audio_data"] and isinstance(item["audio_data"], bytes):
                    item["audio_data"] = base64.b64encode(item["audio_data"]).decode("utf-8")

            return jsonify(audio_chunk)

        return render_template("index.html")

    @staticmethod
    def add_news():
        if request.method == "POST":
            news_service = NewsService()

            # Handle image upload separately
            if "img" in request.files:
                image_data = request.files.get("img").read()
                # Store in app context for later use
                current_app.config["TEMP_IMAGE_DATA"] = image_data
                return "success"

            # Process main form submission
            category = request.form["category"]
            title = request.form["title"]
            desc = request.form["messenge"]

            # Get image data from app context or default
            image_data = current_app.config.get("TEMP_IMAGE_DATA", b"")
            # Clear temporary storage
            current_app.config["TEMP_IMAGE_DATA"] = None

            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%Y-%m-%d")

            news_data = {"category": category, "title": title, "date": formatted_date, "cover": image_data, "desc": desc}

            news_service.add_news(news_data)
            flash("News added successfully", "success")
            return redirect(url_for("news.list"))

        return render_template("news.html")

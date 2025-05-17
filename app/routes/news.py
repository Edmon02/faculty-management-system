# app/routes/news.py
from datetime import datetime

from flask import Blueprint, jsonify, render_template, request, session

from app.services.news_service import NewsService
from app.utils.helpers import login_required

news_bp = Blueprint("news", __name__)


@news_bp.route("/news", methods=["GET"])
def get_news():
    news_service = NewsService()

    if request.headers.get("X-React-Frontend"):
        news = news_service.get_all_news()
        return jsonify(news)
    else:
        return render_template("index.html")


@news_bp.route("/news/<int:id>", methods=["GET"])
def get_news_by_id(id):
    news_service = NewsService()

    if request.headers.get("X-React-Frontend"):
        news = news_service.get_news_by_id(id)
        return jsonify(news)
    else:
        return render_template("index.html")


@news_bp.route("/audio/<int:news_id>/<int:chunk_id>", methods=["GET"])
def get_audio_chunk(news_id, chunk_id):
    news_service = NewsService()

    if request.headers.get("X-React-Frontend"):
        audio_chunk = news_service.get_audio_chunk(news_id, chunk_id)
        return jsonify(audio_chunk)
    else:
        return render_template("index.html")


@news_bp.route("/add-news", methods=["GET", "POST"])
@login_required
def add_news():
    news_service = NewsService()

    if request.method == "POST":
        if "img" in request.files:
            image_data = request.files.get("img").read()
            news_service.set_image_data(image_data)
            return "success"

        category = request.form["category"]
        title = request.form["title"]
        desc = request.form["messenge"]

        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d")

        news_service.add_news(category, title, formatted_date, desc)

    return render_template("news.html")

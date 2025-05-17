# app/services/news_service.py
import base64
from datetime import datetime
from typing import Dict, List, Optional

from app.models.news import News


class NewsService:
    @staticmethod
    def get_all_news() -> List[Dict]:
        """
        Get all news articles, sorted by date (newest first).

        Returns:
            List of news data dictionaries
        """
        news_items = News.query.order_by(News.date.desc()).all()

        # Convert to dictionaries with base64-encoded images
        result = []
        for item in news_items:
            news_dict = item.to_dict()

            # Convert binary data to base64
            if news_dict["cover"] and isinstance(news_dict["cover"], bytes):
                news_dict["cover"] = base64.b64encode(news_dict["cover"]).decode("utf-8")

            result.append(news_dict)

        return result

    @staticmethod
    def get_news_by_id(news_id: int) -> Optional[Dict]:
        """
        Get a news article by ID.

        Args:
            news_id: The news article ID

        Returns:
            News data dictionary or None if not found
        """
        news = News.query.filter_by(id=news_id).first()

        if not news:
            return None

        news_dict = news.to_dict()

        # Convert binary data to base64
        if news_dict["cover"] and isinstance(news_dict["cover"], bytes):
            news_dict["cover"] = base64.b64encode(news_dict["cover"]).decode("utf-8")

        # Handle audio data
        if news_dict.get("audio") and isinstance(news_dict["audio"], bytes):
            news_dict["audio"] = base64.b64encode(news_dict["audio"]).decode("utf-8")

        return news_dict

    @staticmethod
    def create_news(data: Dict) -> int:
        """
        Create a new news article.

        Args:
            data: Dictionary containing news data

        Returns:
            ID of the newly created news article
        """
        news = News(category=data.get("category"), title=data.get("title"), date=data.get("date", datetime.now().strftime("%Y-%m-%d")), cover=data.get("cover"), desc=data.get("desc"))
        news.save()
        return news.id

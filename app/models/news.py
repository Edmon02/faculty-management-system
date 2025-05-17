# app/models/news.py
from datetime import datetime
from typing import Any, Dict

from app import db


class News(db.Model):
    """News article model"""

    __tablename__ = "News"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, default=datetime.now().date)
    cover = db.Column(db.LargeBinary)
    desc = db.Column(db.Text)
    audio = db.Column(db.LargeBinary, nullable=True)

    # Relationships
    audio_chunks = db.relationship("AudioChunk", backref="news", lazy="dynamic")

    def to_dict(self, include_binary: bool = False) -> Dict[str, Any]:
        """Convert news data to dictionary"""
        result = {"id": self.id, "category": self.category, "title": self.title, "date": self.date.strftime("%Y-%m-%d"), "desc": self.desc}

        if include_binary:
            import base64

            result["cover"] = base64.b64encode(self.cover).decode("utf-8") if self.cover else None
            result["audio"] = base64.b64encode(self.audio).decode("utf-8") if self.audio else None

        return result

    def __repr__(self) -> str:
        return f"<News {self.title}>"


class AudioChunk(db.Model):
    """Audio chunk model for storing podcast-like content"""

    __tablename__ = "audio_chunk"

    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey("News.id"), nullable=False)
    chunk_id = db.Column(db.Integer, nullable=False)
    audio_data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self) -> str:
        return f"<AudioChunk {self.news_id}-{self.chunk_id}>"

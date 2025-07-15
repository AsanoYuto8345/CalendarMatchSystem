#backend/database/models/community.py
"""
コミュニティモデル定義
作成者: 遠藤信輝
"""

from app import db

class CommunityModel(db.Model):
    __tablename__ = "communities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)
    
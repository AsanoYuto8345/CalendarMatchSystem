# backend/database/models/template_tag.py
"""
テンプレートタグモデル定義
作成者: 遠藤信輝
"""

from app import db

class TemplateTagModel(db.Model):
    __tablename__ = "template_tags"

    id = db.Column(db.String(100), primary_key=True)
    community_id = db.Column(db.String(100), db.ForeignKey("communities.id"), nullable=False)
    tag = db.Column(db.String(100), nullable=False)
    color_code = db.Column(db.String(6), nullable=False, default="000000")  # ← 追加（#RRGGBB形式）

    community = db.relationship("CommunityModel", backref="template_tags")

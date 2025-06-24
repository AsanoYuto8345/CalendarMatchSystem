"""
テンプレートタグモデル定義
"""

from app import db

class TemplateTagModel(db.Model):
    __tablename__ = "template_tags"

    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=False)
    tag = db.Column(db.String(100), nullable=False)

    community = db.relationship("CommunityModel", backref="template_tags")

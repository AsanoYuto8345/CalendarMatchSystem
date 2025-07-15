# backend/database/models/member.py
"""
コミュニティメンバー定義
作成者: 遠藤信輝
"""
from app import db

class MemberModel(db.Model):
    __tablename__ = "members"
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    community_id = db.Column(db.String, db.ForeignKey("communities.id"), nullable=False)

    community = db.relationship("CommunityModel", backref="member_list")

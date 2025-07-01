# backend/database/models/member.py
from app import db

class MemberModel(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=False)

    community = db.relationship("CommunityModel", backref="member_list")

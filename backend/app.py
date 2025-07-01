from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# SQLite 設定
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)

# 「最初のリクエスト前に一度だけ実行する」代わりに、
# before_request とフラグを使って初回のみ DB を作成・初期化する
db_initialized = False

@app.before_request
def init_db():
    global db_initialized
    if not db_initialized:
        db.create_all()
        if Message.query.count() == 0:
            db.session.add_all([
                Message(text="Hello from Flask!"),
                Message(text="SQLite と React のサンプルです！")
            ])
            db.session.commit()
        db_initialized = True

@app.route("/api/messages")
def get_messages():
    msgs = Message.query.all()
    return jsonify([{"id": m.id, "text": m.text} for m in msgs])

from modules.community_service.route import community_bp as community_service_bp
from modules.community_management.route import management_bp as community_management_bp

app.register_blueprint(community_service_bp, url_prefix="/api/community")
app.register_blueprint(community_management_bp, url_prefix="/api/community/manage")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
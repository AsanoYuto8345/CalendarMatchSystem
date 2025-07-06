from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
# ← ここを変更
from extentions import db
import os

app = Flask(__name__)
CORS(app)

# SQLite 設定
app.config["SQLALCHEMY_DATABASE_URI"]      = "sqlite:///messages.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ← こうする
db.init_app(app)

class Message(db.Model):
    id   = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)


db_initialized = False

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    return send_from_directory(uploads_dir, filename, as_attachment=False)

@app.before_request
def init_db():
    global db_initialized
    if not db_initialized:
        # アプリコンテキストが必要
        with app.app_context():
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
from modules.user_data_process.route import user_data_bp
from modules.user_data_management.route import user_bp
from modules.calendar_process.route import calendar_bp
from modules.calendar_manager.route import calendar_manager_bp
from modules.Loginout.route import auth_bp ,init_app
from modules.matching.route import matching_bp
# Blueprint の登録

app.register_blueprint(auth_bp)
app.register_blueprint(calendar_bp)
app.register_blueprint(calendar_manager_bp)
app.register_blueprint(community_service_bp, url_prefix="/api/community")
app.register_blueprint(community_management_bp)
app.register_blueprint(user_data_bp) # C3 ユーザ情報処理部のBlueprintを登録
app.register_blueprint(user_bp)      # C8 ユーザ情報管理部のBlueprintを登録
app.register_blueprint(matching_bp)

init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

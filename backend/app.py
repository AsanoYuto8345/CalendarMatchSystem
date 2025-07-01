from flask import Flask, jsonify
from flask_cors import CORS
# ← ここを変更
from extentions import db  

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

# Blueprint の登録
from modules.calendar_manager.route import calendar_manager_bp
app.register_blueprint(calendar_manager_bp)
from modules.calendar_process.route import calendar_bp
app.register_blueprint(calendar_bp)

@app.route("/api/messages")
def get_messages():
    msgs = Message.query.all()
    return jsonify([{"id": m.id, "text": m.text} for m in msgs])

@app.route("/api/community/<string:communityId>", methods=["GET"])
def get_community_name(communityId):
    return jsonify({"community_name": "仮コミュニティ名", "communityId": communityId})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

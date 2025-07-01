# backend/database/models/community.py

"""
C4 コミュニティ処理部
作成者: 遠藤信輝
"""

from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os

community_bp = Blueprint("community", __name__)

# アップロードフォルダ
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# コミュニティモデル - dbインスタンスを遅延取得
def get_db():
    """アプリケーションコンテキストからdbインスタンスを取得"""
    return current_app.extensions['sqlalchemy']

# グローバル変数でモデルクラスをキャッシュ
_community_model = None

def get_community_model():
    """コミュニティモデルクラスを取得（キャッシュ付き）"""
    global _community_model
    
    if _community_model is not None:
        return _community_model
    
    db = get_db()
    
    # モデルクラスを動的に作成
    class CommunityModel(db.Model):
        __tablename__ = "communities"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), unique=True, nullable=False)
        image_path = db.Column(db.String(200), nullable=True)
    
    _community_model = CommunityModel
    return _community_model

def create_community_table():
    """コミュニティテーブルを作成"""
    db = get_db()
    get_community_model()  # モデルを登録
    db.create_all()

@community_bp.before_request
def log_request():
    """リクエスト内容をログ出力する"""
    print(f"🔍 {request.method} {request.path}")
    print(f"🔍 Content-Type: {request.content_type}")
    print(f"🔍 Content-Length: {request.content_length}")

# M2: コミュニティ作成
@community_bp.route("/community/create", methods=["GET", "POST", "OPTIONS"])
@cross_origin()
def community_create():
    print("=" * 50)
    print("✅ /community/create にアクセスが来ました")

    if request.method == 'OPTIONS':
        return '', 200
    if request.method == 'GET':
        return jsonify({"message": "GET request received"})

    try:
        db = get_db()
        CommunityModel = get_community_model()
        
        # テーブルが存在しない場合は作成
        create_community_table()
        
        community_name = request.form.get('community_name', '').strip()
        image_file = request.files.get('image')

        if not community_name:
            return jsonify({"error": "コミュニティ名が入力されていません"}), 400
        if len(community_name) > 16:
            return jsonify({"error": "コミュニティ名は16文字以内で入力してください"}), 400
        if CommunityModel.query.filter_by(name=community_name).first():
            return jsonify({"error": "その名前のコミュニティは既に存在します"}), 409

        saved_filename = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(filepath)
            saved_filename = filename
            print(f"✅ 画像保存成功: {filepath}")

        new_community = CommunityModel(name=community_name, image_path=saved_filename)
        db.session.add(new_community)
        db.session.commit()

        return jsonify({
            "message": f"コミュニティ '{community_name}' を作成しました",
            "community_name": community_name,
            "image_uploaded": saved_filename is not None,
            "image_filename": saved_filename
        }), 200

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": f"サーバーエラー: {str(e)}"}), 500
    finally:
        print("=" * 50)

# M3: コミュニティ参加
@community_bp.route("/community/join", methods=["POST"])
@cross_origin()
def community_join():
    print("✅ /community/join にアクセスが来ました")
    try:
        CommunityModel = get_community_model()
        
        data = request.get_json() or {}
        community_name = data.get("community_name", "").strip()
        if not community_name:
            return jsonify({"error": "コミュニティ名が未入力です"}), 400
        community = CommunityModel.query.filter_by(name=community_name).first()
        if not community:
            return jsonify({"error": f"コミュニティ '{community_name}' は存在しません"}), 404
        return jsonify({"message": f"コミュニティ '{community_name}' に参加しました"}), 200
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": f"サーバーエラー: {str(e)}"}), 500

# M4: コミュニティ脱退
@community_bp.route("/community/leave", methods=["POST"])
@cross_origin()
def community_leave():
    print("✅ /community/leave にアクセスが来ました")
    try:
        CommunityModel = get_community_model()
        
        data = request.get_json() or {}
        user_id = data.get("id", "").strip()
        community_id = data.get("community_id", "").strip()
        if not user_id or not community_id:
            return jsonify({"error": "ユーザIDまたはコミュニティIDが未入力です"}), 400
        community = CommunityModel.query.get(community_id)
        if not community:
            return jsonify({"error": f"ID {community_id} のコミュニティは存在しません"}), 404
        print(f"🧹 ユーザ {user_id} をコミュニティ {community_id} から脱退しました（仮）")
        return jsonify({
            "message": f"ユーザ '{user_id}' はコミュニティ '{community.name}' を脱退しました",
            "result": True
        }), 200
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": f"サーバーエラー: {str(e)}"}), 500

# M5: テンプレートタグ編集
@community_bp.route("/community/edit_tags", methods=["POST"])
@cross_origin()
def edit_template_tags():
    print("✅ /community/edit_tags にアクセスが来ました")
    try:
        data = request.get_json() or {}
        user_id = data.get("id", "").strip()
        tags = data.get("tsg_list", [])
        operation = data.get("operation", "").strip()
        if not user_id or not operation:
            return jsonify({"error": "ユーザIDまたは操作内容が未入力です"}), 400
        if operation not in ["add", "edit", "delete"]:
            return jsonify({"error": f"無効な操作です: {operation}"}), 400
        print(f"🛠️ タグを {operation} 処理しました（仮）")
        return jsonify({
            "message": f"タグを {operation} 処理しました",
            "operation": operation,
            "tag_count": len(tags),
            "result": True
        }), 200
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": f"サーバーエラー: {str(e)}"}), 500
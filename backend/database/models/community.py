"""
C4 コミュニティ処理部
作成者: 遠藤信輝
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

community_bp = Blueprint("community", __name__)
db = SQLAlchemy()

# コミュニティモデル
class Community(db.Model):
    __tablename__ = "communities"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@community_bp.before_request
def log_request():
    """リクエスト内容をログ出力する"""
    print(f"🔍 {request.method} {request.path}")
    print(f"🔍 Content-Type: {request.content_type}")
    print(f"🔍 Content-Length: {request.content_length}")

class CommunityMain:
    """
    M1 コミュニティ主処理
    C1 UI処理部より操作リクエストを受け取り、action_type に応じて処理関数へ分配する
    """
    def handle_request(self, id, community_name, action_type, tags=None):
        if not id or not community_name or not action_type:
            return {"error": "必要な入力が不足しています"}, 400

        if action_type == "create":
            return community_create_main(id, community_name)
        elif action_type == "join":
            return community_join_main(id, community_name)
        elif action_type == "leave":
            return community_leave_main(id, community_name)
        elif action_type == "edit":
            return edit_template_tags(id, tags)
        else:
            return {"error": "不正なアクションタイプです"}, 400

@community_bp.route("/community/create", methods=["GET", "POST", "OPTIONS"])
@cross_origin()
def community_create():
    """
    M2 コミュニティ作成

    GET: フロントからの動作確認用レスポンスを返す
    POST: フォームデータからコミュニティを作成
    """
    print("=" * 50)
    print("✅ /community/create にアクセスが来ました")

    if request.method == 'OPTIONS':
        return '', 200

    if request.method == 'GET':
        return jsonify({"message": "GET request received"})

    try:
        community_name = request.form.get('community_name', '').strip()
        image_file = request.files.get('image')

        if not community_name:
            return jsonify({"error": "コミュニティ名が入力されていません"}), 400

        if len(community_name) > 16:
            return jsonify({"error": "コミュニティ名は16文字以内で入力してください"}), 400

        if Community.query.filter_by(name=community_name).first():
            return jsonify({"error": "その名前のコミュニティは既に存在します"}), 409

        saved_filename = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(filepath)
            saved_filename = filename
            print(f"✅ 画像保存成功: {filepath}")

        new_community = Community(name=community_name, image_path=saved_filename)
        db.session.add(new_community)
        db.session.commit()

        return jsonify({
            "message": f"コミュニティ '{community_name}' を作成しました",
            "community_name": community_name,
            "image_uploaded": saved_filename is not None,
            "image_filename": saved_filename
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"サーバーエラー: {str(e)}"}), 500
    finally:
        print("=" * 50)

@community_bp.route("/community/join", methods=["POST"])
@cross_origin()
def community_join():
    """
    M3 コミュニティ参加

    JSONで受け取った名前をもとに参加処理
    """
    print("✅ /community/join にアクセスが来ました")

    try:
        data = request.get_json()
        community_name = data.get("community_name", "").strip()

        print(f"📦 受け取った community_name: '{community_name}'")

        if not community_name:
            return jsonify({"error": "コミュニティ名が未入力です"}), 400

        community = Community.query.filter_by(name=community_name).first()
        if not community:
            return jsonify({"error": f"コミュニティ '{community_name}' は存在しません"}), 404

        return jsonify({
            "message": f"コミュニティ '{community_name}' に参加しました"
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"サーバーエラー: {str(e)}"}), 500

@community_bp.route("/community/leave", methods=["POST"])
@cross_origin()
def community_leave():
    """
    M4 コミュニティ脱退

    指定されたユーザIDとコミュニティIDに基づいて脱退処理を行う。
    """
    print("✅ /community/leave にアクセスが来ました")

    try:
        data = request.get_json()
        user_id = data.get("id", "").strip()
        community_id = data.get("community_id", "").strip()

        print(f"📦 受信: user_id = '{user_id}', community_id = '{community_id}'")

        if not user_id or not community_id:
            return jsonify({"error": "ユーザIDまたはコミュニティIDが未入力です"}), 400

        # 仮に存在確認（※必要に応じてUserモデルが必要）
        community = Community.query.filter_by(id=community_id).first()
        if not community:
            return jsonify({"error": f"ID {community_id} のコミュニティは存在しません"}), 404

        # 実際の脱退処理（DB上でユーザとコミュニティの関係を切る処理が必要）
        # ※仮実装
        print(f"🧹 ユーザ {user_id} をコミュニティ {community_id} から脱退させる処理を実行（仮）")

        return jsonify({
            "message": f"ユーザ '{user_id}' はコミュニティ '{community.name}' を脱退しました",
            "result": True
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"サーバーエラー: {str(e)}"}), 500

@community_bp.route("/community/edit_tags", methods=["POST"])
@cross_origin()
def edit_template_tags():
    """
    M5 テンプレートタグ編集処理

    指定されたユーザIDとタグリスト、および操作種別に応じて
    テンプレートタグを追加・編集・削除する。
    """
    print("✅ /community/edit_tags にアクセスが来ました")

    try:
        data = request.get_json()
        user_id = data.get("id", "").strip()
        tags = data.get("tsg_list", [])
        operation = data.get("operation", "").strip()

        print(f"📦 受信: user_id = '{user_id}', operation = '{operation}'")
        print(f"📦 タグリスト: {tags}")

        if not user_id or not operation:
            return jsonify({"error": "ユーザIDまたは操作内容が未入力です"}), 400

        if operation not in ["add", "edit", "delete"]:
            return jsonify({"error": f"無効な操作です: {operation}"}), 400

        # タグの存在チェックや重複確認・更新処理などは
        # 実装次第でタグモデルが必要です（仮実装とする）

        print(f"🛠️ テンプレートタグを {operation} 処理（仮）実行")

        return jsonify({
            "message": f"タグを {operation} 処理しました",
            "operation": operation,
            "tag_count": len(tags),
            "result": True
        }), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"サーバーエラー: {str(e)}"}), 500

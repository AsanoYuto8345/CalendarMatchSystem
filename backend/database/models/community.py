"""
C4 コミュニティ処理部
作成者: 遠藤信輝

- M2: コミュニティ作成
- M3: コミュニティ参加
- M4: コミュニティ脱退
- M5: テンプレートタグ操作
"""

from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os
import logging

# Blueprint 定義
community_bp = Blueprint("community", __name__)
logger = logging.getLogger(__name__)

# アップロードフォルダ設定
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# DB インスタンス遅延取得

def get_db():
    """
    アプリケーションコンテキストから SQLAlchemy インスタンスを取得する
    """
    return current_app.extensions['sqlalchemy']

# モデルクラスキャッシュ
_community_model = None

def get_community_model():
    """
    コミュニティモデルクラスを返却（キャッシュ付き）
    """
    global _community_model
    if _community_model:
        return _community_model

    db = get_db()
    class CommunityModel(db.Model):
        __tablename__ = "communities"
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), unique=True, nullable=False)
        image_path = db.Column(db.String(200), nullable=True)
    _community_model = CommunityModel
    return _community_model


def create_community_table():
    """
    コミュニティテーブルが存在しない場合に作成する
    """
    db = get_db()
    get_community_model()  # モデル登録
    db.create_all()

@community_bp.before_request
def log_request():
    """
    全リクエストのメソッド・パスおよびヘッダーサイズをログ出力する
    """
    logger.debug(f"🔍 {request.method} {request.path}")
    logger.debug(f"🔍 Content-Type: {request.content_type}")
    logger.debug(f"🔍 Content-Length: {request.content_length}")


# M2: コミュニティ作成
@community_bp.route("/community/create", methods=["OPTIONS", "GET", "POST"])
@cross_origin()
def community_create():
    """
    コミュニティの新規作成を行う

    OPTIONS: CORS プリフライト対応
    GET: 確認用テストエンドポイント
    POST: コミュニティ名および画像ファイルを受け取り登録
    """
    logger.info("✅ /community/create accessed")
    if request.method == 'OPTIONS':
        return '', 200
    if request.method == 'GET':
        return jsonify({"message": "GET request received"}), 200

    try:
        # DB 準備
        db = get_db()
        CommunityModel = get_community_model()
        create_community_table()

        # フォームデータ取得
        community_name = request.form.get('community_name', '').strip()
        image_file = request.files.get('image')

        # 入力バリデーション
        if not community_name:
            return jsonify({"error": "コミュニティ名が入力されていません"}), 400
        if len(community_name) > 16:
            return jsonify({"error": "コミュニティ名は16文字以内で入力してください"}), 400
        if CommunityModel.query.filter_by(name=community_name).first():
            return jsonify({"error": "その名前のコミュニティは既に存在します"}), 409

        # 画像保存
        saved_filename = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image_file.save(filepath)
            saved_filename = filename
            logger.info(f"✅ Image saved: {filepath}")

        # レコード登録
        new_comm = CommunityModel(name=community_name, image_path=saved_filename)
        db.session.add(new_comm)
        db.session.commit()

        return jsonify({
            "message": f"コミュニティ '{community_name}' を作成しました",
            "community_name": community_name,
            "image_uploaded": bool(saved_filename),
            "image_filename": saved_filename
        }), 201

    except Exception as e:
        logger.exception('Error during community_create')
        return jsonify({"error": f"サーバーエラー: {e}"}), 500


# M3: コミュニティ参加
@community_bp.route("/community/join", methods=["POST"])
@cross_origin()
def community_join():
    """
    指定されたコミュニティ名で参加処理を行う
    """
    logger.info("✅ /community/join accessed")
    try:
        CommunityModel = get_community_model()
        data = request.get_json() or {}
        community_name = data.get("community_name", "").strip()

        if not community_name:
            return jsonify({"error": "コミュニティ名が未入力です"}), 400

        comm = CommunityModel.query.filter_by(name=community_name).first()
        if not comm:
            return jsonify({"error": f"コミュニティ '{community_name}' は存在しません"}), 404

        return jsonify({"message": f"コミュニティ '{community_name}' に参加しました"}), 200

    except Exception as e:
        logger.exception('Error during community_join')
        return jsonify({"error": f"サーバーエラー: {e}"}), 500


# M4: コミュニティ脱退
@community_bp.route("/community/leave", methods=["POST"])
@cross_origin()
def community_leave():
    """
    指定ユーザを指定コミュニティから脱退させる
    """
    logger.info("✅ /community/leave accessed")
    try:
        CommunityModel = get_community_model()
        data = request.get_json() or {}
        user_id = data.get("id", "").strip()
        community_id = data.get("community_id", "").strip()

        if not user_id or not community_id:
            return jsonify({"error": "ユーザIDまたはコミュニティIDが未入力です"}), 400

        comm = CommunityModel.query.get(community_id)
        if not comm:
            return jsonify({"error": f"ID {community_id} のコミュニティは存在しません"}), 404

        logger.info(f"🧹 User {user_id} left community {community_id}")
        return jsonify({"message": f"ユーザ '{user_id}' はコミュニティ '{comm.name}' を脱退しました","result": True}), 200

    except Exception as e:
        logger.exception('Error during community_leave')
        return jsonify({"error": f"サーバーエラー: {e}"}), 500


# M5: テンプレートタグ操作
@community_bp.route("/community/template_tags", methods=["GET", "POST", "PUT", "DELETE"])
@cross_origin()
def template_tags():
    """
    テンプレートタグの一覧取得・追加・更新・削除を行う
    """
    try:
        # --- GET: タグ一覧取得 ---
        if request.method == 'GET':
            community_id = request.args.get('community_id', '').strip()
            if not community_id:
                return jsonify({"error": "コミュニティIDが未指定です"}), 400

            # TODO: DBから get_template_tags(community_id) を呼び出して一覧取得
            tags = []
            logger.info(f"✅ GET /community/template_tags community_id={community_id}")
            return jsonify({"tags": tags}), 200

        # --- POST/PUT/DELETE: JSON ボディから取得 ---
        data = request.get_json() or {}
        community_id = data.get('community_id', '').strip()
        template_tag_id = data.get('template_tag_id', '').strip()
        if not community_id or not template_tag_id:
            return jsonify({"error": "コミュニティIDまたはテンプレートタグIDが未指定です"}), 400

        if request.method == 'POST':
            logger.info(f"✅ POST /community/template_tags community_id={community_id}, template_tag_id={template_tag_id}")
            # TODO: add_template_tag(community_id, template_tag_id)
            return jsonify({"message": "タグを追加しました", "template_tag_id": template_tag_id, "result": True}), 201

        if request.method == 'PUT':
            logger.info(f"✅ PUT /community/template_tags community_id={community_id}, template_tag_id={template_tag_id}")
            # TODO: update_template_tag(community_id, template_tag_id)
            return jsonify({"message": "タグを更新しました", "template_tag_id": template_tag_id, "result": True}), 200

        if request.method == 'DELETE':
            logger.info(f"✅ DELETE /community/template_tags community_id={community_id}, template_tag_id={template_tag_id}")
            # TODO: remove_template_tag(community_id, template_tag_id)
            return jsonify({"message": "タグを削除しました", "template_tag_id": template_tag_id, "result": True}), 200

        # 許可外メソッド
        return jsonify({"error": "許可されていないメソッドです"}), 405

    except Exception as e:
        logger.exception('Error during template_tags')
        return jsonify({"error": f"サーバーエラー: {e}"}), 500

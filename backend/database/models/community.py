"""
C4 コミュニティ処理部
作成者: 遠藤信輝
"""

from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os
import logging

community_bp = Blueprint("community", __name__)
logger = logging.getLogger(__name__)

# アップロードフォルダ
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# dbインスタンスを遅延取得

def get_db():
    """アプリケーションコンテキストからdbインスタンスを取得"""
    return current_app.extensions['sqlalchemy']

# モデルクラスのキャッシュ
_community_model = None

def get_community_model():
    """コミュニティモデルクラスを取得（キャッシュ付き）"""
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
    """コミュニティテーブルを作成"""
    db = get_db()
    get_community_model()
    db.create_all()

@community_bp.before_request
def log_request():
    """リクエスト内容をログ出力"""
    logger.debug(f"🔍 {request.method} {request.path}")
    logger.debug(f"🔍 Content-Type: {request.content_type}")
    logger.debug(f"🔍 Content-Length: {request.content_length}")

# M2: コミュニティ作成
@community_bp.route("/community/create", methods=["GET","POST","OPTIONS"])
@cross_origin()
def community_create():
    logger.info("✅ /community/create にアクセスが来ました")
    if request.method == 'OPTIONS':
        return '', 200
    if request.method == 'GET':
        return jsonify({"message": "GET request received"}), 200

    try:
        db = get_db()
        CommunityModel = get_community_model()
        create_community_table()

        community_name = request.form.get('community_name','').strip()
        image_file = request.files.get('image')

        if not community_name:
            return jsonify({"error":"コミュニティ名が入力されていません"}),400
        if len(community_name)>16:
            return jsonify({"error":"コミュニティ名は16文字以内で入力してください"}),400
        if CommunityModel.query.filter_by(name=community_name).first():
            return jsonify({"error":"その名前のコミュニティは既に存在します"}),409

        saved_filename=None
        if image_file and image_file.filename:
            fn=secure_filename(image_file.filename)
            path=os.path.join(UPLOAD_FOLDER,fn)
            image_file.save(path)
            saved_filename=fn
            logger.info(f"✅ 画像保存成功: {path}")

        new_comm=CommunityModel(name=community_name,image_path=saved_filename)
        db.session.add(new_comm)
        db.session.commit()
        return jsonify({
            "message":f"コミュニティ '{community_name}' を作成しました",
            "community_name":community_name,
            "image_uploaded":bool(saved_filename),
            "image_filename":saved_filename
        }),201
    except Exception as e:
        logger.exception('コミュニティ作成中にエラー')
        return jsonify({"error":f"サーバーエラー:{e}"}),500

# M3: コミュニティ参加
@community_bp.route("/community/join",methods=["POST"])
@cross_origin()
def community_join():
    logger.info("✅ /community/join にアクセスが来ました")
    try:
        CommunityModel=get_community_model()
        data=request.get_json() or {}
        name=data.get("community_name","").strip()
        if not name:
            return jsonify({"error":"コミュニティ名が未入力です"}),400
        comm=CommunityModel.query.filter_by(name=name).first()
        if not comm:
            return jsonify({"error":f"コミュニティ '{name}' は存在しません"}),404
        return jsonify({"message":f"コミュニティ '{name}' に参加しました"}),200
    except Exception as e:
        logger.exception('参加処理中にエラー')
        return jsonify({"error":f"サーバーエラー:{e}"}),500

# M4: コミュニティ脱退
@community_bp.route("/community/leave",methods=["POST"])
@cross_origin()
def community_leave():
    logger.info("✅ /community/leave にアクセスが来ました")
    try:
        CommunityModel=get_community_model()
        data=request.get_json() or {}
        user_id=data.get("id","").strip()
        community_id=data.get("community_id","").strip()
        if not user_id or not community_id:
            return jsonify({"error":"ユーザIDまたはコミュニティIDが未入力です"}),400
        comm=CommunityModel.query.get(community_id)
        if not comm:
            return jsonify({"error":f"ID {community_id} のコミュニティは存在しません"}),404
        logger.info(f"🧹 ユーザ {user_id} をコミュニティ {community_id} から脱退しました(仮)")
        return jsonify({"message":f"ユーザ '{user_id}' はコミュニティ '{comm.name}' を脱退しました","result":True}),200
    except Exception as e:
        logger.exception('脱退処理中にエラー')
        return jsonify({"error":f"サーバーエラー:{e}"}),500

# M5: テンプレートタグ操作
@community_bp.route("/community/template_tags",methods=["GET","POST","PUT","DELETE"])
@cross_origin()
def template_tags():
    """テンプレートタグの一覧取得・追加・更新・削除"""
    try:
        if request.method=='GET':
            community_id=request.args.get('community_id','').strip()
            if not community_id:
                return jsonify({"error":"コミュニティIDが未指定です"}),400
            # TODO: DBから取得
            tags=[]
            logger.info(f"✅ GET /community/template_tags (community_id={community_id})")
            return jsonify({"tags":tags}),200

        data=request.get_json() or {}
        community_id=data.get('community_id','').strip()
        tags=data.get('tsg_list',[])
        if not community_id:
            return jsonify({"error":"コミュニティIDが未指定です"}),400

        if request.method=='POST':
            logger.info(f"✅ POST /community/template_tags (community_id={community_id},tsg_list={tags})")
            return jsonify({"message":"タグを追加しました","tag_count":len(tags)}),201

        if request.method=='PUT':
            logger.info(f"✅ PUT /community/template_tags (community_id={community_id},tsg_list={tags})")
            return jsonify({"message":"タグを更新しました","tag_count":len(tags)}),200

        if request.method=='DELETE':
            logger.info(f"✅ DELETE /community/template_tags (community_id={community_id},tsg_list={tags})")
            return jsonify({"message":"タグを削除しました","tag_count":len(tags)}),200

        return jsonify({"error":"許可されていないメソッドです"}),405
    except Exception as e:
        logger.exception('テンプレートタグ操作中にエラー')
        return jsonify({"error":f"サーバーエラー:{e}"}),500

# modules/community_service/community_service.py（最小限の修正）
import os
import logging
from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)
# 今すぐこれに置き換えてください
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../uploads'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    """Flaskアプリのコンテキスト内で安全にdbを取得"""
    try:
        _ = current_app._get_current_object()
    except RuntimeError as e:
        raise RuntimeError("Flaskアプリケーションコンテキストが存在しません") from e

    # current_appを通じてdbインスタンスを取得
    return current_app.extensions['sqlalchemy']

def create_community():
    try:
        db = get_db()

        # モデルの初期化（初回のみ）
        if not hasattr(current_app, '_community_model_created'):
            class CommunityModel(db.Model):
                __tablename__ = "communities"
                id = db.Column(db.Integer, primary_key=True)
                name = db.Column(db.String(100), unique=True, nullable=False)
                image_path = db.Column(db.String(200), nullable=True)

            db.create_all()
            current_app._community_model_created = True
            current_app._CommunityModel = CommunityModel

        CommunityModel = current_app._CommunityModel

        name = request.form.get("community_name", "").strip()
        image_file = request.files.get("image")
        print(f"📨 リクエスト受信: community_name={name}, image_file={image_file}")

        if not name:
            return jsonify({"error": "コミュニティ名が入力されていません"}), 400
        if len(name) > 16:
            return jsonify({"error": "16文字以内にしてください"}), 400

        if CommunityModel.query.filter_by(name=name).first():
            return jsonify({"error": "既に存在します"}), 409

        filename = None
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            print(f"📁 アップロードパス: {save_path}")
            try:
                image_file.save(save_path)
                print("✅ 画像保存成功")
            except Exception as e:
                print(f"❌ 画像保存失敗: {e}")
                return jsonify({"error": "画像の保存に失敗しました"}), 500
        else:
            print("ℹ️ 画像は指定されていません")

        new_comm = CommunityModel(name=name, image_path=filename)
        db.session.add(new_comm)
        db.session.commit()
        print(f"🆕 コミュニティ作成: {name}（画像: {filename}）")

        return jsonify({
            "message": f"'{name}' を作成しました",
            "community_name": name,
            "image_uploaded": bool(filename),
            "image_filename": filename
        }), 201

    except Exception as e:
        logger.exception("create_community failed")
        db = get_db()
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

def join_community():
    try:
        db = get_db()
        
        # モデルを取得（既に作成されている前提）
        if hasattr(current_app, '_CommunityModel'):
            CommunityModel = current_app._CommunityModel
        else:
            return jsonify({"error": "Community model not initialized"}), 500

        data = request.get_json() or {}
        name = data.get("community_name", "").strip()

        if not name:
            return jsonify({"error": "未入力です"}), 400

        comm = CommunityModel.query.filter_by(name=name).first()
        if not comm:
            return jsonify({"error": f"'{name}' は存在しません"}), 404

        return jsonify({"message": f"'{name}' に参加しました"}), 200

    except Exception as e:
        logger.exception("join_community failed")
        return jsonify({"error": str(e)}), 500

def leave_community():
    try:
        db = get_db()
        
        if hasattr(current_app, '_CommunityModel'):
            CommunityModel = current_app._CommunityModel
        else:
            return jsonify({"error": "Community model not initialized"}), 500

        data = request.get_json() or {}
        user_id = data.get("id", "").strip()
        comm_id = data.get("community_id", "").strip()

        if not user_id or not comm_id:
            return jsonify({"error": "ID未入力"}), 400

        try:
            comm_id = int(comm_id)
        except ValueError:
            return jsonify({"error": "無効なコミュニティIDです"}), 400

        comm = CommunityModel.query.get(comm_id)
        if not comm:
            return jsonify({"error": f"{comm_id} は存在しません"}), 404

        return jsonify({
            "message": f"ユーザ '{user_id}' はコミュニティ '{comm.name}' を脱退しました",
            "result": True
        }), 200

    except Exception as e:
        logger.exception("leave_community failed")
        return jsonify({"error": str(e)}), 500

def handle_template_tags():
    try:
        db = get_db()
        
        # テンプレートタグモデルの初期化
        if not hasattr(current_app, '_template_tag_model_created'):
            class TemplateTagModel(db.Model):
                __tablename__ = "template_tags"
                id = db.Column(db.Integer, primary_key=True)
                community_id = db.Column(db.Integer, db.ForeignKey("communities.id"), nullable=False)
                tag = db.Column(db.String(100), nullable=False)
            
            db.create_all()
            current_app._template_tag_model_created = True
            current_app._TemplateTagModel = TemplateTagModel
        
        TemplateTagModel = current_app._TemplateTagModel

        if request.method == 'GET':
            community_id = request.args.get('community_id', '').strip()
            if not community_id:
                return jsonify({"error": "コミュニティIDが未指定です"}), 400

            try:
                community_id = int(community_id)
            except ValueError:
                return jsonify({"error": "無効なコミュニティIDです"}), 400

            tags = TemplateTagModel.query.filter_by(community_id=community_id).all()
            tag_list = [{"id": tag.id, "tag": tag.tag} for tag in tags]
            return jsonify({"tags": tag_list}), 200

        data = request.get_json() or {}
        community_id = data.get('community_id', '').strip()
        template_tag_id = data.get('template_tag_id', '').strip()
        tag_value = data.get('tag', '').strip()

        if not community_id:
            return jsonify({"error": "コミュニティIDが未指定です"}), 400

        try:
            community_id = int(community_id)
        except ValueError:
            return jsonify({"error": "無効なコミュニティIDです"}), 400

        if request.method == 'POST':
            if not tag_value:
                return jsonify({"error": "タグの内容が未指定です"}), 400
            new_tag = TemplateTagModel(community_id=community_id, tag=tag_value)
            db.session.add(new_tag)
            db.session.commit()
            return jsonify({
                "message": "タグを追加しました",
                "template_tag_id": new_tag.id,
                "result": True
            }), 201

        if not template_tag_id:
            return jsonify({"error": "テンプレートタグIDが未指定です"}), 400

        try:
            template_tag_id = int(template_tag_id)
        except ValueError:
            return jsonify({"error": "無効なテンプレートタグIDです"}), 400

        if request.method == 'PUT':
            if not tag_value:
                return jsonify({"error": "タグの内容が未指定です"}), 400
            tag = TemplateTagModel.query.get(template_tag_id)
            if not tag:
                return jsonify({"error": "タグが存在しません"}), 404
            if tag.community_id != community_id:
                return jsonify({"error": "コミュニティIDが一致しません"}), 403
            tag.tag = tag_value
            db.session.commit()
            return jsonify({
                "message": "タグを更新しました",
                "template_tag_id": tag.id,
                "result": True
            }), 200

        if request.method == 'DELETE':
            tag = TemplateTagModel.query.get(template_tag_id)
            if not tag:
                return jsonify({"error": "タグが存在しません"}), 404
            if tag.community_id != community_id:
                return jsonify({"error": "コミュニティIDが一致しません"}), 403
            db.session.delete(tag)
            db.session.commit()
            return jsonify({
                "message": "タグを削除しました",
                "template_tag_id": tag.id,
                "result": True
            }), 200

        return jsonify({"error": "許可されていないメソッドです"}), 405

    except Exception as e:
        logger.exception("handle_template_tags failed")
        db = get_db()
        db.session.rollback()
        return jsonify({"error": f"サーバーエラー: {e}"}), 500
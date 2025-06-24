# C10 カレンダー情報管理部 CalendarManagerクラス  担当: 角田 一颯

from flask_sqlalchemy import SQLAlchemy
from flask import current_app

class Tag(db.Model):
    """
    タグ情報を保持するデータベースモデル
    messages.db に保存されます
    """
    __tablename__ = 'tags' # テーブル名を明確に指定
    # __bind_key__ は指定しない (デフォルトのDBを使用するため)
    id = db.Column(db.String(50), primary_key=True) # タグID
    name = db.Column(db.String(100), unique=True, nullable=False) # 表示名

    def __repr__(self):
        return f"<Tag(id='{self.id}', name='{self.name}')>"

class CalendarManager:
    """
    C10 カレンダー情報管理部

    C5 カレンダー情報処理部からタグ編集、タグ追加、タグ削除の命令を受け、
    DBにアクセスし、DBを更新する。
    """
    def __init__(self, db_instance):
        """
        Args:
            db_instance (SQLAlchemy): Flask-SQLAlchemyのDBインスタンス
        """
        self.db = db_instance

    def tag_add(self, tag_id, tag_name):
        """
        M1 カレンダー情報管理主処理 - タグ追加

        Args:
            tag_id (str): タグID
            tag_name (str): 表示名

        Returns:
            dict: 処理結果 (`result: bool`, `message: str`)
        """
        if not tag_id or not tag_name:
            return {"result": False, "message": "タグIDと表示名は必須です。"}

        # 重複チェック (nameだけでなくidもチェックする方が安全)
        if self.db.session.query(Tag).filter((Tag.id == tag_id) | (Tag.name == tag_name)).first():
            return {"result": False, "message": f"タグID '{tag_id}' または表示名 '{tag_name}' は既に存在します。"}

        try:
            new_tag = Tag(id=tag_id, name=tag_name)
            self.db.session.add(new_tag)
            self.db.session.commit()
            return {"result": True, "message": f"タグ '{tag_name}' (ID: {tag_id}) が追加されました。", "tag": {"id": new_tag.id, "name": new_tag.name}}
        except Exception as e:
            self.db.session.rollback()
            return {"result": False, "message": f"タグの追加に失敗しました: {str(e)}"}

    def tag_delete(self, tag_id, tag_name):
        """
        M1 カレンダー情報管理主処理 - タグ削除

        Args:
            tag_id (str): タグID
            tag_name (str): 表示名

        Returns:
            dict: 処理結果 (`result: bool`, `message: str`)
        """
        if not tag_id or not tag_name:
            return {"result": False, "message": "タグIDと表示名は必須です。"}

        try:
            # tag_id と tag_name の両方が一致するものを削除
            tag_to_delete = self.db.session.query(Tag).filter_by(id=tag_id, name=tag_name).first()

            if not tag_to_delete:
                return {"result": False, "message": f"タグID '{tag_id}' と表示名 '{tag_name}' に一致するタグが見つかりません。"}

            self.db.session.delete(tag_to_delete)
            self.db.session.commit()
            return {"result": True, "message": f"タグ '{tag_name}' (ID: {tag_id}) が削除されました。"}
        except Exception as e:
            self.db.session.rollback()
            return {"result": False, "message": f"タグの削除に失敗しました: {str(e)}"}

    def tag_edit(self, tag_id, new_tag_name):
        """
        M1 カレンダー情報管理主処理 - タグ編集

        Args:
            tag_id (str): 編集するタグのID
            new_tag_name (str): 新しい表示名

        Returns:
            dict: 処理結果 (`result: bool`, `message: str`)
        """
        if not tag_id or not new_tag_name:
            return {"result": False, "message": "タグIDと新しい表示名は必須です。"}

        try:
            tag_to_edit = self.db.session.query(Tag).filter_by(id=tag_id).first()

            if not tag_to_edit:
                return {"result": False, "message": f"タグID '{tag_id}' に一致するタグが見つかりません。"}

            # 新しい表示名が既存の他のタグの名前と重複しないかチェック
            if self.db.session.query(Tag).filter(Tag.name == new_tag_name, Tag.id != tag_id).first():
                return {"result": False, "message": f"表示名 '{new_tag_name}' は既に他のタグで使用されています。"}

            tag_to_edit.name = new_tag_name
            self.db.session.commit()
            return {"result": True, "message": f"タグID '{tag_id}' の表示名が '{new_tag_name}' に更新されました。", "tag": {"id": tag_to_edit.id, "name": tag_to_edit.name}}
        except Exception as e:
            self.db.session.rollback()
            return {"result": False, "message": f"タグの編集に失敗しました: {str(e)}"}

    def get_all_tags(self):
        """
        M1 カレンダー情報管理主処理 - 全タグ取得

        Returns:
            dict: 処理結果 (`result: bool`, `message: str`, `tags: list`)
        """
        try:
            tags = self.db.session.query(Tag).all()
            tag_list = [{"id": tag.id, "name": tag.name} for tag in tags]
            return {"result": True, "message": "タグを正常に取得しました。", "tags": tag_list}
        except Exception as e:
            return {"result": False, "message": f"タグの取得に失敗しました: {str(e)}", "tags": []}
# C10 カレンダー情報管理部 CalendarManagerクラス  担当: 角田 一颯, 浅野勇翔
from extentions import db

class Tag(db.Model):
    """
    タグ情報を保持するデータベースモデル
    messages.db に保存されます
    """
    __tablename__ = 'tags'

    id           = db.Column(db.String(50),  unique=True, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    color        = db.Column(db.String(6),   nullable=False)
    submitter_id = db.Column(db.String(100), nullable=False)
    community_id = db.Column(db.String(100), nullable=False)
    date         = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Tag(id='{self.id}', name='{self.name}')>"

    def to_dict(self):
        """
        この Tag オブジェクトを JSON 化可能な dict に変換する
        """
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "submitter_id": self.submitter_id,
            "community_id": self.community_id,
            "date": self.date
        }


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

    def request_calendar_data(self, community_id, date):
        """
        M2 カレンダー情報要求
        Args:
            community_id (str): コミュニティID
            date (date): 日付
        Returns:
            dict: 処理結果 (data: List[Tag], result: bool, message: str)
        """
        if not community_id or not date:
            return {"result": False, "message": "コミュニティIDと日付は必須です"}

        try:
            tags = Tag.query.filter_by(community_id=community_id).filter_by(date=date).all()
            serialized_tag = [tag.to_dict() for tag in tags]
            return {"data": serialized_tag, "result": True, "message": "タグの検索に成功しました"}
        except Exception as e:
            self.db.session.rollback()
            return {"result": False, "message": f"タグの検索に失敗しました: {str(e)}"}

    def tag_delete(self, tag_id):
        """
        M3 タグ削除要求
        Args:
            tag_id (str): タグID
        Returns:
            dict: 処理結果 (result: bool, message: str)
        """
        if not tag_id:
            return {"result": False, "message": "タグIDと表示名は必須です。"}

        try:
            tag_to_delete = self.db.session.query(Tag).filter_by(id=tag_id).first()
            if not tag_to_delete:
                return {"result": False, "message": f"タグID '{tag_id}' に一致するタグが見つかりません。"}

            self.db.session.delete(tag_to_delete)
            self.db.session.commit()
            return {"result": True, "message": f"タグ 'ID: {tag_id} が削除されました。"}
        except Exception as e:
            self.db.session.rollback()
            return {"result": False, "message": f"タグの削除に失敗しました: {str(e)}"}

    def tag_data_save(self, tag_id, tag_name, tag_color, submitter_id, community_id, date):
        """
        M4 タグ投稿データ保存要求
        Args:
            tag_id (str): タグID
            tag_name (str): 表示名
            tag_color (str): タグのカラーコード
            submitter_id (str): タグ登録者のID
            community_id (str): コミュニティID
            date (str): 日付
        Returns:
            dict: 処理結果 (result: bool, message: str)
        """
        if not tag_id:
            return {"result": False, "message": "tag_id が未指定です"}
        if not tag_name:
            return {"result": False, "message": "tag_name が未指定です"}
        if not tag_color:
            return {"result": False, "message": "tag_color が未指定です"}
        if not submitter_id:
            return {"result": False, "message": "submitter_id が未指定です"}
        if not community_id:
            return {"result": False, "message": "community_id が未指定です"}
        if not date:
            return {"result": False, "message": "date が未指定です"}

        if self.db.session.query(Tag).filter(
            (Tag.date == date) &
            (Tag.submitter_id == submitter_id) &
            (Tag.name == tag_name)
        ).first():
            return {"result": False, "message": "指定された日付、登録者のタグは"}

        try:
            new_tag = Tag(
                id=tag_id,
                name=tag_name,
                color=tag_color,
                submitter_id=submitter_id,
                community_id=community_id,
                date=date
            )
            self.db.session.add(new_tag)
            self.db.session.commit()
            return {
                "result": True,
                "message": f"タグ '{tag_name}' (ID: {tag_id}) が追加されました。",
                "tag": {"id": new_tag.id, "name": new_tag.name}
            }
        except Exception as e:
            self.db.session.rollback()
            return {"result": False, "message": f"タグの追加に失敗しました: {str(e)}"}
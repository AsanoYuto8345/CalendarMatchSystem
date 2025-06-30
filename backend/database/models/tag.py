# Tagのデータベースモデルを定義するclass 作成者: 浅野 勇翔

from app import db

class Tag(db.Model):
    """
    タグ情報を保持するデータベースモデル
    messages.db に保存されます
    """
    __tablename__ = 'tags' # テーブル名を明確に指定
    # __bind_key__ は指定しない (デフォルトのDBを使用するため)
    id = db.Column(db.String(50), unique=True, primary_key=True) # タグID
    name = db.Column(db.String(100), nullable=False) # 表示名
    color = db.Column(db.String(6), nullable=False) # タグのカラーコード
    submitter_id = db.Column(db.String(100), nullable=False) # タグ登録者のID
    community_id = db.Column(db.String(100), nullable=False) # コミュニティID
    date =  db.Column(db.Date, nullable=False) # タグの対象日付け

    def __repr__(self):
        return f"<Tag(id='{self.id}', name='{self.name}')>"
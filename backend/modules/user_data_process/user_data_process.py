# user_data_process.py
# C3 ユーザ情報処理部のM1, M2, M3, M4モジュールを実装したUserProcessクラス
# 作成者: [担当者の名前]

import uuid
import hashlib
import requests # requestsライブラリをインポート
import os # ファイル操作のためにインポート
from werkzeug.utils import secure_filename # ファイル名を安全にするためにインポート

# アップロードされたアイコン画像を保存するルートディレクトリ
# このパスはアプリケーションの実行環境に合わせて適宜変更してください
UPLOAD_ROOT = "uploads/user_icons"


class UserDataProcess:
    """
    C3 ユーザ情報処理部 M1 ユーザデータ主処理
    C1 UI処理部からユーザデータを受け取り、ユーザデータを各処理メソッドで処理し
    C1 UI処理部に返却する
    """

    # C8 ユーザ情報管理部のAPIのベースURLを定義
    # Flaskアプリケーションのmodules/users/route.pyでurl_prefix='/api'が設定されているため、
    # ここではホストとポートのみを指定します。
    C8_API_BASE_URL = "http://localhost:5001"  # Flaskアプリケーションのホストとポートに合わせて変更してください

    def __init__(self):
        """
        コンストラクタ
        """
        # アイコン保存ディレクトリが存在しない場合は作成
        os.makedirs(UPLOAD_ROOT, exist_ok=True)

    def _hash_password(self, password: str) -> str:
        """
        パスワードをハッシュ化するプライベートメソッド
        Args:
            password (str): ハッシュ化するパスワード
        Returns:
            str: ハッシュ化されたパスワード
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def data_regist(self, email: str, password: str, name: str, icon_file=None) -> dict:
        """
        M2 ユーザデータ登録処理
        ユーザIDをランダム生成して、パスワードをハッシュ化してユーザデータの登録を要求する。
        Args:
            email (str): 登録するメールアドレス
            password (str): 登録するパスワード
            name (str): 表示名
            icon_file (FileStorage, optional): アップロードされたアイコンファイル. Defaults to None.
        Returns:
            dict: 処理結果と登録されたユーザデータ。
                    成功時は {"result": True, "user_id": str, "hashed_pw": str, ...}
                    失敗時は {"result": False, "error": str, "status": int}
        """
        # E1: 入力形式の簡易チェック
        if not all([email, password, name]):
            return {"result": False, "error": "入力データが不足しています", "status": 400}

        user_id = str(uuid.uuid4())  # ユーザIDをランダム生成
        hashed_pw = self._hash_password(password)
        icon_name = None  # 初期化

        # アイコンファイルを保存
        if icon_file and icon_file.filename:
            filename = secure_filename(icon_file.filename)
            user_icon_folder = os.path.join(UPLOAD_ROOT, user_id)
            os.makedirs(user_icon_folder, exist_ok=True)
            icon_path_full = os.path.join(user_icon_folder, filename)
            try:
                icon_file.save(icon_path_full)
                icon_name = os.path.join(user_id, filename)  # DBに保存する相対パス
            except Exception as e:
                return {"result": False, "error": f"アイコンファイルの保存に失敗しました: {e}", "status": 500}

        # C8 ユーザ情報管理部への登録を要求
        # エンドポイント: POST /api/users/register
        # 外部設計書 F1 ユーザ情報よりemailもC8に登録するため追加
        register_payload = {
            "id": user_id,
            "hashed_pw": hashed_pw,
            "name": name,
            "email": email,
            "icon": icon_name  # 保存したアイコンのパスを渡す
        }
        try:
            response = requests.post(f"{self.C8_API_BASE_URL}/api/users/register", json=register_payload)
            response_data = response.json()

            if response.status_code == 201:
                return {
                    "result": True,
                    "user_id": user_id,
                    "hashed_pw": hashed_pw,
                    "name": name,
                    "icon_name": icon_name,  # UIに返すアイコン名（パス）
                    "email": email
                }
            elif response.status_code == 409:  # E3: 登録済みデータあり
                # 登録失敗時は保存したアイコンファイルを削除
                if icon_name and os.path.exists(icon_path_full):
                    os.remove(icon_path_full)
                    # フォルダが空なら削除
                    if not os.listdir(user_icon_folder):
                        os.rmdir(user_icon_folder)
                return {"result": False, "error": "すでに存在するユーザIDまたはメールアドレスです", "status": 409}
            else:
                # 登録失敗時は保存したアイコンファイルを削除
                if icon_name and os.path.exists(icon_path_full):
                    os.remove(icon_path_full)
                    if not os.listdir(user_icon_folder):
                        os.rmdir(user_icon_folder)
                return {"result": False, "error": response_data.get("message", "C8でのユーザ登録に失敗しました"), "status": response.status_code}
        except requests.exceptions.RequestException as e:
            # 接続エラー時は保存したアイコンファイルを削除
            if icon_name and os.path.exists(icon_path_full):
                os.remove(icon_path_full)
                if not os.listdir(user_icon_folder):
                    os.rmdir(user_icon_folder)
            return {"result": False, "error": f"C8への接続エラー: {e}", "status": 500}

    def data_edit(self, user_id: str, password: str = None,
                  name: str = None, icon_file=None, email: str = None) -> dict:  # icon_nameをicon_fileに変更
        """
        M3 ユーザデータ編集処理
        変更したパスワードをハッシュ化して、ユーザデータの再登録を要求する。
        Args:
            user_id (str): 編集対象のユーザID
            password (str, optional): 新しいパスワード. Defaults to None.
            name (str, optional): 新しい表示名. Defaults to None.
            icon_file (FileStorage, optional): 新しいアイコンファイル. Defaults to None.
            email (str, optional): 新しいメールアドレス. Defaults to None.
        Returns:
            dict: 処理結果。
                    成功時は {"result": True}
                    失敗時は {"result": False, "error": str, "status": int}
        """
        # E1: 入力形式の簡易チェック
        if not user_id:
            return {"result": False, "error": "ユーザIDが指定されていません", "status": 400}

        update_payload = {"id": user_id}
        current_icon_path = None # 現在のアイコンパスを保持

        # 現在のユーザー情報を取得して現在のアイコンパスを確認
        get_user_response = self.data_get(user_id)
        if get_user_response["result"]:
            current_icon_path = get_user_response["user_data"].get("icon_name")
        elif get_user_response["status"] == 404:
            return {"result": False, "error": "更新対象のユーザが存在しません", "status": 404}


        if password:
            update_payload["hashed_pw"] = self._hash_password(password)
        if name:
            update_payload["name"] = name
        if email:
            update_payload["email"] = email

        # アイコンファイルの処理
        icon_name = None
        if icon_file and icon_file.filename:
            filename = secure_filename(icon_file.filename)
            user_icon_folder = os.path.join(UPLOAD_ROOT, user_id)
            os.makedirs(user_icon_folder, exist_ok=True)
            icon_path_full = os.path.join(user_icon_folder, filename)

            try:
                # 既存のアイコンファイルがあれば削除
                if current_icon_path and os.path.exists(os.path.join(UPLOAD_ROOT, current_icon_path)):
                    os.remove(os.path.join(UPLOAD_ROOT, current_icon_path))
                icon_file.save(icon_path_full)
                icon_name = os.path.join(user_id, filename)  # DBに保存する相対パス
                update_payload["icon"] = icon_name
            except Exception as e:
                return {"result": False, "error": f"新しいアイコンファイルの保存に失敗しました: {e}", "status": 500}
        elif icon_file is False: # アイコンを削除する場合（例: UIから空のファイルが送信された場合など）
            if current_icon_path and os.path.exists(os.path.join(UPLOAD_ROOT, current_icon_path)):
                os.remove(os.path.join(UPLOAD_ROOT, current_icon_path))
                user_icon_folder = os.path.join(UPLOAD_ROOT, user_id)
                if not os.listdir(user_icon_folder): # フォルダが空なら削除
                    os.rmdir(user_icon_folder)
            update_payload["icon"] = None # DBからアイコンパスを削除

        if len(update_payload) == 1:  # user_idだけの場合
            return {"result": False, "error": "更新する情報がありません", "status": 400}

        # C8 ユーザ情報管理部への更新を要求
        # エンドポイント: PUT /api/users/update
        try:
            response = requests.put(f"{self.C8_API_BASE_URL}/api/users/update", json=update_payload)
            response_data = response.json()

            if response.status_code == 200:
                return {"result": True, "icon_name": icon_name} # 更新されたアイコンパスを返す
            elif response.status_code == 404:  # E2: 該当データなし
                return {"result": False, "error": "更新対象のユーザが存在しません", "status": 404}
            else:
                return {"result": False, "error": response_data.get("message", "C8でのユーザ情報編集に失敗しました"), "status": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"result": False, "error": f"C8への接続エラー: {e}", "status": 500}

    def data_get(self, user_id: str) -> dict:
        """
        M4 ユーザデータ取得処理
        ユーザIDを入力から受け取り、ユーザデータを渡す
        Args:
            user_id (str): 取得対象のユーザID
        Returns:
            dict: 処理結果と取得されたユーザデータ。
                    成功時は {"result": True, "user_data": {...}}
                    失敗時は {"result": False, "error": str, "status": int}
        """
        # E1: 入力形式の簡易チェック
        if not user_id:
            return {"result": False, "error": "ユーザIDが指定されていません", "status": 400}

        # C8 ユーザ情報管理部からのデータ取得を要求
        # エンドポイント: GET /api/users/search?id=<user_id>
        try:
            response = requests.get(f"{self.C8_API_BASE_URL}/api/users/search", params={"id": user_id})
            response_data = response.json()

            if response.status_code == 200:
                # C8から返されるキーをC3のuser_data_getの期待する形式にマッピング
                # C8は 'id', 'name', 'email', 'icon' を返す
                # C3は 'user_id', 'email', 'name', 'icon_name' を期待
                icon_path_for_ui = response_data.get("icon")
                if icon_path_for_ui:
                    # UIがアクセスできるパスに変換 (例: /uploads/user_icons/user_id/icon.png)
                    icon_path_for_ui = f"/{UPLOAD_ROOT}/{icon_path_for_ui}"
                else:
                    icon_path_for_ui = "/icons/default_user.png" # デフォルトアイコンのパス

                user_data_mapped = {
                    "user_id": response_data.get("id"),
                    "email": response_data.get("email"),
                    "name": response_data.get("name"),
                    "icon_name": icon_path_for_ui # UIに返すアイコンのパス
                }
                return {"result": True, "user_data": user_data_mapped}
            elif response.status_code == 404:  # E2: 該当データなし
                return {"result": False, "error": "該当するユーザデータがありません", "status": 404}
            else:
                return {"result": False, "error": response_data.get("message", "C8でのユーザ情報取得に失敗しました"), "status": response.status_code}
        except requests.exceptions.RequestException as e:
            return {"result": False, "error": f"C8への接続エラー: {e}", "status": 500}

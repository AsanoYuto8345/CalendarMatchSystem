# C3 ユーザ情報処理部のM1, M2, M3, M4モジュールを実装したUserProcessクラス
# 作成者: [担当者の名前]

import uuid
import hashlib

class UserDataProcess:
    """
    C3 ユーザ情報処理部 M1 ユーザデータ主処理
    C1 UI処理部からユーザデータを受け取り、ユーザデータを各処理メソッドで処理し
    C1 UI処理部に返却する
    """

    def __init__(self):
        """
        コンストラクタ
        """
        pass

    def _hash_password(self, password: str) -> str:
        """
        パスワードをハッシュ化するプライベートメソッド
        Args:
            password (str): ハッシュ化するパスワード
        Returns:
            str: ハッシュ化されたパスワード
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def data_regist(self, email: str, password: str, name: str, icon_name: str) -> dict:
        """
        M2 ユーザデータ登録処理
        ユーザIDをランダム生成して、パスワードをハッシュ化してユーザデータの登録を要求する。
        Args:
            email (str): 登録するメールアドレス
            password (str): 登録するパスワード
            name (str): 表示名
            icon_name (str): アイコンのファイル名
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

        # C8 ユーザ情報管理部への登録をシミュレート
        # 実際にはC8のAPIを呼び出す
        # 例: C8_user_management_api.register_user(user_id, hashed_pw, name, icon_name)
        # ここでは成功を仮定
        is_registered_in_c8 = True # C8との連携結果を仮定
        if not is_registered_in_c8:
            # E3: 登録済みデータあり (ここではUUID生成なので通常発生しないが、想定として)
            return {"result": False, "error": "すでに存在するユーザIDです", "status": 409}

        return {
            "result": True,
            "user_id": user_id,
            "hashed_pw": hashed_pw,
            "name": name,
            "icon_name": icon_name
        }

    def data_edit(self, user_id: str, password: str = None, 
                  name: str = None, icon_name: str = None) -> dict:
        """
        M3 ユーザデータ編集処理
        変更したパスワードをハッシュ化して、ユーザデータの再登録を要求する。
        Args:
            user_id (str): 編集対象のユーザID
            password (str, optional): 新しいパスワード. Defaults to None.
            name (str, optional): 新しい表示名. Defaults to None.
            icon_name (str, optional): 新しいアイコンのファイル名. Defaults to None.
        Returns:
            dict: 処理結果。
                  成功時は {"result": True}
                  失敗時は {"result": False, "error": str, "status": int}
        """
        # E1: 入力形式の簡易チェック
        if not user_id:
            return {"result": False, "error": "ユーザIDが指定されていません", "status": 400}

        update_data = {}
        if password:
            update_data["hashed_pw"] = self._hash_password(password)
        if name:
            update_data["name"] = name
        if icon_name:
            update_data["icon_name"] = icon_name
        
        if not update_data:
            return {"result": False, "error": "更新する情報がありません", "status": 400}

        # C8 ユーザ情報管理部への更新をシミュレート
        # 実際にはC8のAPIを呼び出す
        # 例: C8_user_management_api.update_user(user_id, update_data)
        # ここでは成功を仮定し、対象のユーザが存在することを仮定
        user_exists_in_c8 = True # C8でのユーザ存在チェックを仮定
        if not user_exists_in_c8:
            # E2: 該当データなし
            return {"result": False, "error": "更新対象のユーザが存在しません", "status": 404}
            
        is_updated_in_c8 = True # C8との連携結果を仮定
        if not is_updated_in_c8:
             # C8で更新失敗した場合のエラー (C8からの具体的なエラーコードは要相談)
            return {"result": False, "error": "ユーザ情報の更新に失敗しました", "status": 500}


        return {"result": True}

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

        # C8 ユーザ情報管理部からのデータ取得をシミュレート
        # 実際にはC8のAPIを呼び出す
        # 例: user_data = C8_user_management_api.get_user(user_id)
        # ここでは仮のデータを返す
        mock_user_data = {
            "user_id": user_id,
            "email": f"user_{user_id}@example.com",
            "name": f"TestUser_{user_id}",
            "icon_name": "default.png"
        }
        
        # E2: 該当データなし
        if user_id not in ["mock_user_1", "mock_user_2"]: # 存在しないIDの例
            return {"result": False, "error": "該当するユーザデータがありません", "status": 404}

        return {"result": True, "user_data": mock_user_data}

# modules/Loginout/user_auth.py
# C2 ユーザ認証処理部
# 担当: 石田めぐみ

import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
import requests # <-- requestsモジュールをインポート（HTTP通信用）
import json     # <-- JSONデータを扱うため
import os # 環境変数アクセス用に追加

# --- C2 内部コンポーネント: パスワードハッシュ処理 ---
# このセクションは C2 の内部で利用されるパスワードハッシュ処理を定義します。

class PasswordHasher:
    """
    パスワードハッシュ処理の抽象基底クラス。
    実際のアプリケーションでは、よりセキュアなライブラリ (例: bcrypt, argon2-cffi) を使用する。
    """

    def hash_password(self, password: str) -> str:
        """
        指定されたパスワードをハッシュ化する。

        Args:
            password (str): ハッシュ化するプレーンテキストのパスワード。

        Returns:
            str: ハッシュ化されたパスワード。
        """
        raise NotImplementedError

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        プレーンテキストのパスワードとハッシュ化されたパスワードを比較する。

        Args:
            password (str): 比較するプレーンテキストのパスワード。
            hashed_password (str): 比較対象のハッシュ化されたパスワード。

        Returns:
            bool: パスワードが一致すれば True、そうでなければ False。
        """
        raise NotImplementedError


class SHA256PasswordHasher(PasswordHasher):
    """
    SHA256 を使用した簡易的なパスワードハッシュ実装。
    開発環境向けであり、本番環境では使用しないこと。
    """

    def hash_password(self, password: str) -> str:
        """
        パスワードをSHA256でハッシュ化する。

        Args:
            password (str): ユーザーのパスワード。

        Returns:
            str: SHA256ハッシュ値。
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        パスワードとSHA256ハッシュ値を比較する。

        Args:
            password (str): ユーザーが入力したパスワード。
            hashed_password (str): 保存されているハッシュ値。

        Returns:
            bool: パスワードが一致すれば True。
        """
        return self.hash_password(password) == hashed_password


# --- C2 内部コンポーネント: セッションストア ---
# このセクションは C2 の内部で利用されるアクティブセッション管理を定義します。

class SessionStore:
    """
    セッションストアの抽象基底クラス。
    セッションの作成、取得、削除のインターフェースを定義する。
    """

    def create_session(self, user_id: str, session_id: str, expires_at: datetime) -> None:
        """
        新しいセッションをストアに追加する。

        Args:
            user_id (str): セッションに関連付けるユーザーID。
            session_id (str): C8 から発行されたセッションID。
            expires_at (datetime): セッションの有効期限。
        """
        raise NotImplementedError

    def get_user_id(self, session_id: str) -> str | None:
        """
        セッションIDからユーザーIDを取得する。
        セッションが無効または期限切れの場合は None を返す。

        Args:
            session_id (str): 検索するセッションID。

        Returns:
            str | None: ユーザーID、または None。
        """
        raise NotImplementedError

    def delete_session(self, session_id: str) -> bool:
        """
        指定されたセッションIDのセッションを削除する。

        Args:
            session_id (str): 削除するセッションID。

        Returns:
            bool: 削除が成功すれば True、セッションが見つからなければ False。
        """
        raise NotImplementedError


class InMemorySessionStore(SessionStore):
    """
    インメモリのセッションストア実装。
    開発用途に限定し、本番環境では Redis やデータベースを使用すること。
    """

    def __init__(self):
        """
        InMemorySessionStore のコンストラクタ。
        セッションデータを格納する辞書を初期化する。
        """
        self._sessions = {}  # {session_id: {"user_id": ..., "expires_at": ...}}

    def create_session(self, user_id: str, session_id: str, expires_at: datetime) -> None:
        """
        新しいセッションをインメモリに保存する。

        Args:
            user_id (str): セッションに関連付けるユーザーID。
            session_id (str): C8 から発行されたセッションID。
            expires_at (datetime): セッションの有効期限。
        """
        self._sessions[session_id] = {"user_id": user_id, "expires_at": expires_at}


    def get_user_id(self, session_id: str) -> str | None:
        """
        セッションIDに対応するユーザーIDを取得する。
        セッションが存在しないか、有効期限切れの場合は None を返す。

        Args:
            session_id (str): クライアントから提供されたセッションID。

        Returns:
            str | None: 該当するユーザーID、または None。
        """
        session_info = self._sessions.get(session_id)
        if session_info and session_info["expires_at"] > datetime.now():
            return session_info["user_id"]
        # 有効期限切れまたは存在しないセッションはクリーンアップ（任意）
        if session_id in self._sessions:
            del self._sessions[session_id]
        return None

    def delete_session(self, session_id: str) -> bool:
        """
        インメモリからセッションを削除する。

        Args:
            session_id (str): 削除するセッションID。

        Returns:
            bool: 削除が成功すれば True、該当セッションがなければ False。
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            return True
        return False


# --- C2 ユーザ認証処理部 本体 ---

class UserAuth:
    """
    C2 ユーザ認証処理部。
    C1 UI処理部よりユーザデータを受け取り、ユーザデータを各処理関数に渡す。
    ログイン処理、ログアウト処理、認証主処理を担う。
    """

    def __init__(
        self,
        session_store: SessionStore,
        password_hasher: PasswordHasher,
        http_client: Any = requests
    ):
        """
        UserAuth のコンストラクタ。
        セッションストア、パスワードハッシャー、HTTPクライアントのインスタンスを受け取る。

        Args:
            session_store (SessionStore): セッション管理のためのストア実装。
            password_hasher (PasswordHasher): パスワードハッシュ処理の実装。
            http_client (Any): HTTP通信を行うためのクライアント。（例: requestsモジュール）
        """
        self.session_store = session_store
        self.password_hasher = password_hasher
        self.http_client = http_client

        # 環境変数からC8のベースURLを取得。設定されていない場合はデフォルト値を使用。
        self.C8_BASE_URL = os.environ.get("C8_BASE_URL", "http://localhost:8000/c8")


    def handle_auth(self, url: str) -> tuple[int, str]:
        """
        M1 認証主処理:
        入力されたURLの形式チェックなどを行い、結果を返却する。

        入力:
            url (String): 入力されたURL。 (入力元: ブラウザ)

        出力:
            status (Integer): ステータスコード。 (出力先: C1 UI処理部)
                - 200: 正常
                - 400: 入力エラー (E1) - URL形式不正
            sid (String): セッションID。 (出力先: C1 UI処理部)
                - 正常時に生成されるダミーセッションID

        エラー処理:
            処理フラグや入力データ形式が不正の場合、入力エラーとしてステータスコード400を返す。(E1)
        """
        if not isinstance(url, str) or not url.startswith("http"):
            return 400, ""

        try:
            payload = {"user_id": "dummy_user_id_for_auth"}
            response = self.http_client.post(f"{self.C8_BASE_URL}/make_sid", json=payload)
            response.raise_for_status()

            response_data = response.json()
            sid = response_data.get("session_id", "")

            if sid:
                return 200, sid
            else:
                print("Error: C8 did not return a session ID for handle_auth.")
                return 500, ""
        except Exception as e: # requests.exceptions.RequestException を Exception に変更
            print(f"Error calling C8 make_sid for handle_auth: {e}")
            return 500, ""
        # json.JSONDecodeError は RequestException のサブクラスではないため、
        # もし JSONDecodeError を個別に捕捉したい場合は、Exception の前に記述する必要がある
        # ただし、requests.exceptions.RequestException が多くのネットワーク関連エラーをカバーするため、
        # 通常はそれらを含めて Exception で捕捉すれば十分
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from C8 response for handle_auth: {e}")
            return 500, ""


    def signin_user(self, email: str, pw: str) -> tuple[bool, str]:
        """
        M2 ログイン処理：
        ユーザID (メールアドレス) とパスワードを検証し、成功時にセッションIDを発行する。

        入力:
            email (String): メールアドレス。 (入力元: C1 UI処理部)
            pw (String): パスワード。 (入力元: C1 UI処理部)

        出力:
            result (bool): 処理の成否 (false: エラー, true: 正常)。 (出力先: C1 UI処理部)
            sid (String): セッションID。 (出力先: C1 UI処理部)

        エラー処理:
            検索対象のデータが該当しなかった場合、検索対象のデータが登録済みデータに存在しないことを報告し、`result=False` を返す。（E2）
        """
        if not email or not pw:
            print("Warning: Email or password cannot be empty for signin.")
            return False, ""

        user_info = None
        try:
            # C8のget_user_by_emailエンドポイントを呼び出し
            response = self.http_client.get(f"{self.C8_BASE_URL}/users_by_email/{email}")
            
            # C8が204 (No Content) を返した場合、ユーザーは存在しない
            if response.status_code == 204:
                print(f"Authentication failed: User with email '{email}' not found.")
                return False, ""
            
            response.raise_for_status() # それ以外のHTTPエラーがあれば例外を発生させる

            user_info = response.json()
            user_id = user_info.get("user_id")
            hashed_password = user_info.get("hashed_password")

            if not user_id or not hashed_password:
                print(f"Error: Incomplete user data from C8 for email: {email}")
                return False, ""
                
        except Exception as e: # requests.exceptions.HTTPError などをまとめて Exception に変更
            print(f"Error during C8 user info retrieval for email {email}: {e}")
            return False, ""
        except json.JSONDecodeError as e:
            # C8からのレスポンスが不正なJSONだった場合
            print(f"Error decoding JSON from C8 get_user_by_email: {e}")
            return False, ""


        if not self.password_hasher.verify_password(pw, user_info.get("hashed_password", "")):
            print("Authentication failed: Invalid password.")
            return False, ""

        # 認証成功: C8 を使ってセッションIDを作成し、永続化する
        session_id = ""
        try:
            payload = {"user_id": user_info["user_id"]}
            response = self.http_client.post(f"{self.C8_BASE_URL}/make_sid", json=payload)
            response.raise_for_status()

            response_data = response.json() 
            session_id = response_data.get("session_id", "")

            if not session_id:
                print("Error: C8 did not return a session ID after successful user authentication.")
                return False, "" # C8がSIDを返さなかった場合

        except Exception as e: # requests.exceptions.HTTPError などをまとめて Exception に変更
            print(f"Error during C8 SID creation for user {user_info.get('user_id', 'N/A')}: {e}")
            return False, ""
        except json.JSONDecodeError as e:
            # C8からのレスポンスが不正なJSONだった場合
            print(f"Error decoding JSON from C8 make_sid: {e}")
            return False, ""
        

        # 全てのtry-exceptブロックを抜けて、SIDが正常に取得できた場合のみ実行
        self.session_store.create_session(user_info["user_id"], session_id, datetime.now() + timedelta(hours=1))
        return True, session_id


    def signout_user(self, sid: str) -> bool:
        """
        M3 ログアウト処理：
        セッションIDを受け取り、そのセッションを破棄することでログアウトを行う。

        入力:
            sid (String): セッションID。

        出力:
            result (bool): 処理の成否 (false: エラー, true: 正常)。
        """
        if not sid:
            print("Warning: Attempted to sign out with an empty SID.")
            return False

        success_persistent_delete = False
        try:
            response = self.http_client.delete(f"{self.C8_BASE_URL}/delete_sid/{sid}")
            response.raise_for_status()
            if response.status_code in [200, 204]: # 204 No Content も成功とみなす
                success_persistent_delete = True
        except Exception as e: # requests.exceptions.HTTPError などをまとめて Exception に変更
            print(f"Error calling C8 delete_sid: {e}")
            success_persistent_delete = False
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from C8 delete_sid: {e}")
            success_persistent_delete = False


        success_in_memory_delete = self.session_store.delete_session(sid)

        # C8での削除に成功したか、内部セッションストアでの削除に成功したか、どちらかでOK
        return success_persistent_delete or success_in_memory_delete
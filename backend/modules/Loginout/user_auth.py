# modules/Loginout/user_auth.py
# C2 ユーザ認証処理部
# 担当: 石田めぐみ

import hashlib
from typing import Any, Optional
import requests
import json
import os
import logging

# ログ設定（開発用としてINFOレベルで設定）
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- C2 内部コンポーネント: パスワードハッシュ処理 ---

class PasswordHasher:
    """
    パスワードハッシュ処理の抽象基底クラス。
    実際のアプリケーションでは、よりセキュアなライブラリ (例: bcrypt, argon2-cffi) を使用する。
    """

    def hash_password(self, password: str) -> str:
        """
        指定されたパスワードをハッシュ化する。
        """
        raise NotImplementedError

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        プレーンテキストのパスワードとハッシュ化されたパスワードを比較する。
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
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        パスワードとSHA256ハッシュ値を比較する。
        """
        return self.hash_password(password) == hashed_password


# --- C2 ユーザ認証処理部 本体 ---

class UserAuth:
    """
    C2 ユーザ認証処理部。
    C1 UI処理部よりユーザデータを受け取り、ユーザデータを各処理関数に渡す。
    ログイン処理、ログアウト処理、認証主処理を担う。
    セッションの永続管理はC8に、クライアント側の状態管理はフロントエンドに完全に委ねる。
    """

    def __init__(
        self,
        password_hasher: PasswordHasher,
        http_client: Any = requests
    ):
        """
        UserAuth のコンストラクタ。
        パスワードハッシャー、HTTPクライアントのインスタンスを受け取る。
        """
        self.password_hasher = password_hasher
        self.http_client = http_client

        # 環境変数からC8のベースURLを取得。設定されていない場合はデフォルト値を使用。
        self.C8_BASE_URL = os.environ.get("C8_BASE_URL", "http://localhost:8000/api")


    def handle_auth(self, url: str) -> tuple[int, str]:
        """
        M1 認証主処理:
        入力されたURLの形式チェックなどを行い、結果を返却する。
        """
        if not isinstance(url, str) or not url.startswith("http"):
            logger.warning(f"Invalid URL format or type: {url}")
            return 400, ""

        try:
            # ダミーメールアドレスを使いSIDを作成する（C8の仕様に合わせてエンドポイント修正）
            payload = {"mail": "dummy@example.com"}
            response = self.http_client.post(f"{self.C8_BASE_URL}/sid/create", json=payload)
            response.raise_for_status()

            response_data = response.json()
            sid = response_data.get("sid", "")

            if sid:
                logger.info(f"SID generated successfully for handle_auth: {sid}")
                return 200, sid
            else:
                logger.error("C8 did not return a session ID for handle_auth.")
                return 500, ""
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling C8 sid/create for handle_auth: {e}")
            return 500, ""
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from C8 response for handle_auth: {e}")
            return 500, ""
        except Exception as e:
            logger.error(f"Unexpected error in handle_auth: {e}")
            return 500, ""


    def create_sid_for_user(self, email: str) -> Optional[str]:
        """
        C8のSID作成API呼び出し。
        """
        try:
            payload = {"mail": email}
            response = self.http_client.post(f"{self.C8_BASE_URL}/sid/create", json=payload)
            response.raise_for_status()
            data = response.json()
            sid = data.get("sid")
            if sid:
                logger.info(f"SID created for user {email}: {sid}")
                return sid
            else:
                logger.error(f"No SID returned from C8 for user {email}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating SID for user {email}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating SID for user {email}: {e}")
            return None


    def signin_user(self, email: str, pw: str) -> tuple[bool, str]:
        """
        M2 ログイン処理：
        C8にメールアドレスで直接ユーザー検索APIがないため、暫定的に
        emailの前半部分をユーザIDとしてC8のユーザー検索APIを呼ぶ例。
        パスワード検証は現状C8のAPI仕様上不可能なためFalseを返す。
        """
        user_id_guess = email.split("@")[0]

        try:
            response = self.http_client.get(f"{self.C8_BASE_URL}/users/search", params={"id": user_id_guess})

            if response.status_code == 404:
                logger.warning(f"User not found: {user_id_guess}")
                return False, ""

            response.raise_for_status()
            user_info = response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving user info: {e}")
            return False, ""
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from C8 user info: {e}")
            return False, ""
        except Exception as e:
            logger.error(f"Unexpected error retrieving user info: {e}")
            return False, ""

        # パスワード検証はC8 API仕様上できないため認証失敗として扱う
        logger.error("Password verification not implemented due to C8 API limitations.")
        return False, ""


    def signout_user(self, sid: str) -> bool:
        """
        M3 ログアウト処理：
        C8のSID削除APIを呼び出す。
        """
        try:
            response = self.http_client.delete(f"{self.C8_BASE_URL}/sid/delete", json={"sid": sid})
            if response.status_code in [200, 204]:
                logger.info(f"SID '{sid}' deleted successfully.")
                return True
            else:
                logger.error(f"Unexpected status code {response.status_code} on SID deletion.")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting SID '{sid}': {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting SID '{sid}': {e}")
            return False

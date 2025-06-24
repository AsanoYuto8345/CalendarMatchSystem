# modules/Loginout/user_auth.py
# C2 ユーザ認証処理部
# 担当: 石田めぐみ

import uuid # このモジュールは不要になるが、念のため残しておく
import hashlib
from datetime import datetime, timedelta # timedeltaは不要になるが、念のため残しておく
from typing import Any, Dict, Optional
import requests
import json
import os
import logging

# ログ設定（開発用としてINFOレベルで設定）
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        # session_store: SessionStore, # SessionStoreは不要になったため削除
        password_hasher: PasswordHasher,
        http_client: Any = requests
    ):
        """
        UserAuth のコンストラクタ。
        パスワードハッシャー、HTTPクライアントのインスタンスを受け取る。
        """
        # self.session_store = session_store # SessionStoreは不要になったため削除
        self.password_hasher = password_hasher
        self.http_client = http_client

        # 環境変数からC8のベースURLを取得。設定されていない場合はデフォルト値を使用。
        self.C8_BASE_URL = os.environ.get("C8_BASE_URL", "http://localhost:8000/c8")


    def handle_auth(self, url: str) -> tuple[int, str]:
        """
        M1 認証主処理:
        入力されたURLの形式チェックなどを行い、結果を返却する。
        設計書におけるM1の機能概要に沿うが、E2エラー（ユーザー検索）はM1の役割ではないため実装しない。

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
            C8との通信エラーやJSONパースエラー、C8がSIDを返さない場合は500を返す。
        """
        # 設計書 (M1) の E1: 入力データ形式不正のチェック
        # NOTE: 設計書に寄せるため、厳密なURLバリデーションではなく、
        # 設計書に記載された「URL形式不正」の簡易チェックにとどめます。
        if not isinstance(url, str) or not url.startswith("http"):
            logger.warning(f"Invalid URL format or type: {url}")
            return 400, ""

        try:
            payload = {"user_id": "dummy_user_id_for_auth"}
            response = self.http_client.post(f"{self.C8_BASE_URL}/make_sid", json=payload)
            response.raise_for_status()

            response_data = response.json()
            sid = response_data.get("session_id", "")

            if sid:
                logger.info(f"SID generated successfully for handle_auth: {sid}")
                return 200, sid
            else:
                logger.error("C8 did not return a session ID for handle_auth.")
                return 500, ""
        except Exception as e: # モックとの互換性のため、汎用Exceptionで捕捉
            logger.error(f"Error calling C8 make_sid for handle_auth: {e}")
            return 500, ""
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from C8 response for handle_auth: {e}")
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
            パスワード不一致の場合も`result=False`を返す。
            C8との通信エラーやSID生成失敗の場合も`result=False`を返す。
        """
        # NOTE: 設計書に空入力チェックの明示的な記述がないため、コードから削除した状態を維持します。
        #       これにより、空のemail/pwが渡された場合、後続のrequests呼び出しでエラーになる可能性があります。
        # if not email or not pw:
        #     logger.warning("Email or password cannot be empty for signin.")
        #     return False, ""

        user_info = None
        try:
            # C8のget_user_by_emailエンドポイントを呼び出し
            response = self.http_client.get(f"{self.C8_BASE_URL}/users_by_email/{email}")
            
            # C8が204 (No Content) を返した場合、ユーザーは存在しない（設計書E2に該当）
            if response.status_code == 204:
                logger.warning(f"Authentication failed: User with email '{email}' not found.")
                return False, ""
            
            response.raise_for_status() # それ以外のHTTPエラーがあれば例外を発生させる

            user_info = response.json()
            user_id = user_info.get("user_id")
            hashed_password = user_info.get("hashed_password")

            if not user_id or not hashed_password:
                logger.error(f"Error: Incomplete user data from C8 for email: {email}")
                return False, ""
                
        except Exception as e: # モックとの互換性のため、汎用Exceptionで捕捉
            logger.error(f"Error during C8 user info retrieval for email {email}: {e}")
            return False, ""
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from C8 get_user_by_email: {e}")
            return False, ""


        # パスワードの検証
        if not self.password_hasher.verify_password(pw, user_info.get("hashed_password", "")):
            logger.warning("Authentication failed: Invalid password.")
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
                logger.error("C8 did not return a session ID after successful user authentication.")
                return False, "" # C8がSIDを返さなかった場合

        except Exception as e: # モックとの互換性のため、汎用Exceptionで捕捉
            logger.error(f"Error during C8 SID creation for user {user_info.get('user_id', 'N/A')}: {e}")
            return False, ""
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from C8 make_sid: {e}")
            return False, ""
        
        # セッションIDをC8から取得し、フロントエンドに返すのがC2の役割。
        # C2内でのセッション情報のキャッシュは行いません。
        logger.info(f"User '{user_info['user_id']}' signed in successfully. SID: {session_id}")
        return True, session_id


    def signout_user(self, sid: str) -> bool:
        """
        M3 ログアウト処理：
        セッションIDを受け取り、そのセッションを破棄することでログアウトを行う。
        C8にセッション削除を依頼し、その結果を返す。
        C2では内部セッションストアからの削除は行わない。

        入力:
            sid (String): セッションID。

        出力:
            result (bool): 処理の成否 (false: エラー, true: 正常)。

        エラー処理:
            C8でのSID削除に失敗した場合、result=Falseを返す。
        """
        # NOTE: 設計書に空SIDチェックの明示的な記述がないため、コードから削除した状態を維持します。
        #       これにより、空のsidが渡された場合、後続のrequests呼び出しでエラーになる可能性があります。
        # if not sid:
        #     logger.warning("Attempted to sign out with an empty SID.")
        #     return False

        try:
            # C8のセッションを削除するAPIを呼び出す
            response = self.http_client.delete(f"{self.C8_BASE_URL}/delete_sid/{sid}")
            response.raise_for_status() # HTTPエラー（4xx, 5xx）があれば例外を発生させる

            # C8が200 OKまたは204 No Contentを返せば成功とみなす
            if response.status_code in [200, 204]:
                logger.info(f"SID '{sid}' successfully deleted from C8.")
                return True # C8での削除が成功したためTrueを返す
            else:
                logger.error(f"Unexpected status code from C8 delete_sid for SID '{sid}': {response.status_code} - {response.text}")
                return False # 予期せぬステータスコードは失敗

        except Exception as e: # C8との通信エラー、JSONパースエラーなどを捕捉
            logger.error(f"Failed to delete SID '{sid}' from C8: {e}")
            return False # C8との通信自体が失敗した場合はFalse
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from C8 delete_sid for SID '{sid}': {e}")
            return False # C8からのレスポンスが不正なJSONだった場合もFalse
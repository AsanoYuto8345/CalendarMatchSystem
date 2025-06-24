# modules/Loginout/user_auth.py
# C2 ユーザ認証処理部
# 担当: 石田めぐみ

import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Any

# C8 ユーザー情報管理部をインポート
# !!!この行をコメントアウトまたは削除してください!!!
# from modules.users.user_data_management import UserDataManagement


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
        user_data_manager: Any
    ):
        """
        UserAuth のコンストラクタ。
        セッションストア、パスワードハッシャー、C8 ユーザー情報管理部のインスタンスを受け取る。

        Args:
            session_store (SessionStore): セッション管理のためのストア実装。
            password_hasher (PasswordHasher): パスワードハッシュ処理の実装。
            user_data_manager (Any): C8 ユーザー情報管理部のインスタンス。（実際の型はUserDataManagement）
        """
        self.session_store = session_store
        self.password_hasher = password_hasher
        self.user_data_manager = user_data_manager

    def handle_auth(self, url: str) -> tuple[int, str]:
        """
        M1 認証主処理:
        入力されたURLの形式チェックなどを行い、結果を返却する。
        （設計書に基づき、URLの形式チェックを行うが、認証ロジックは含まない）

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
            検索対象のデータが該当しなかった場合、検索対象のデータが登録済みデータに存在しないことを報告し、404を返す。（E2）
            ※ M1 の設計書ではE2はURLとは直接関連しないため、ここではURL形式不正 (E1) のみ考慮。
                E2は M2 ログイン処理で発生しうるエラーと解釈。
        """
        if not isinstance(url, str) or not url.startswith("http"):
            # E1: URL形式不正
            return 400, "" # ステータスコード, セッションID or エラーメッセージ

        # 正常: ダミーセッションIDを生成 (設計書に「ダミーセッションIDを生成」とあるため)
        # 実際には、このメソッドで認証済みセッションのチェックを行う場合、
        # 既存のセッションIDを検証し、有効であればそのセッションIDを返す
        # ここでは設計書に沿って新規生成
        # user_data_manager を使ってSIDを生成するよう修正しました
        sid = self.user_data_manager.make_sid("dummy_user_id_for_auth") # M1設計書の指示に合わせてダミーIDを使用
        return 200, sid


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
            検索対象のデータが該当しなかった場合、検索対象のデータが登録済みデータに存在しないことを報告し、404を返す。（E2）
            ※ここでは `result=False` と `sid=""` でエラーを示す。
        """
        # 入力値の基本的なチェック (追加)
        if not email or not pw:
            return False, ""

        # C8 ユーザー情報管理部からユーザー情報を取得
        user_info = self.user_data_manager.get_user_by_email(email)

        if not user_info:
            # E2: 検索対象のデータが該当しなかった場合 (ユーザーが見つからない)
            return False, ""

        # パスワードの検証 (ハッシュ化されたパスワードと比較)
        if not self.password_hasher.verify_password(pw, user_info["hashed_password"]):
            # E2: パスワード不一致も認証情報不一致として扱う
            return False, ""

        # 認証成功: C8 を使ってセッションIDを作成し、永続化する
        session_id = self.user_data_manager.make_sid(user_info["user_id"])
        if session_id:
            # C2 内部のセッションストアにもアクティブセッションとして登録（有効期限管理のため）
            self.session_store.create_session(user_info["user_id"], session_id, datetime.now() + timedelta(hours=1)) # 例: 1時間有効
            return True, session_id
        else:
            # セッションIDの生成に失敗した場合 (例: 既にSIDが存在する場合など)
            return False, ""


    def signout_user(self, sid: str) -> bool:
        """
        M3 ログアウト処理：
        セッションIDを受け取り、そのセッションを破棄することでログアウトを行う。

        入力:
            sid (String): セッションID。 (入力元: M1)
                ※ M1 は認証主処理なので、実際にはUI (C1) から受け取ると解釈。

        出力:
            result (bool): 処理の成否 (false: エラー, true: 正常)。 (出力先: C1 UI処理部)
        """
        if not sid:
            # 無効なセッションIDの場合 (空文字列など)
            return False

        # C8 を使ってセッションIDを永続ストレージから削除
        success_persistent_delete = self.user_data_manager.delete_sid(sid)
        # C2 内部のセッションストアからもアクティブセッションを削除
        success_in_memory_delete = self.session_store.delete_session(sid)

        # どちらか一方ででも成功すれば、処理としては成功とみなす
        # より厳密には、両方成功する必要があるが、設計書に合わせてbool単一の返却
        return success_persistent_delete or success_in_memory_delete
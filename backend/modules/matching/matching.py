# C6マッチング処理部の機能が実装されたMatchingクラスを定義するプログラム 作成者: 浅野勇翔

import requests
from typing import List


class Matching:
    """
    C6 マッチング処理部
    """
    
    def __init__(self, base_url: str = "http://localhost:5001"):
        """
        Args:
            base_url (str): API サーバーのベース URL
        """
        self.base_url = base_url.rstrip("/")

        
    def find_matching_user(
        self,
        community_id: str,
        tag_name: str,
        date: str,
        registered_user_id: str
    ) -> List[str]:
        """
        M6 マッチングユーザー取得処理

        指定された community_id, tag_name, date に一致し、
        registered_user_id 以外が投稿したタグのうち、
        通知未送信(notified=False) のものをフィルタして
        submitter_id の一覧を返す。

        Args:
            community_id (str):       コミュニティID
            tag_name (str):           タグ名
            date (str):               日付（'YYYY-MM-DD'形式）
            registered_user_id (str): 自分自身のユーザーID

        Returns:
            List[str]: 通知未送信のタグを投稿したユーザーIDのリスト。
                       エラーや該当なしの場合は空リストを返す。
        """
        endpoint = f"{self.base_url}/api/calendar-manager/find/matching_tags"
        payload = {
            "community_id":        community_id,
            "tag_name":            tag_name,
            "date":                date,
            "registered_user_id":  registered_user_id
        }

        try:
            resp = requests.get(endpoint, json=payload)
            resp.raise_for_status()
            data = resp.json()
        except Exception:
            # 通信エラーやHTTPエラー時は空リスト
            return []

        if not data.get("result", False):
            # API が失敗を返したときも空リスト
            return []

        submitter_ids = [
            tag["submitter_id"]
            for tag in data.get("data", [])
            if not tag.get("notified", False)
        ]
        return submitter_ids
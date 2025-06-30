# C5 カレンダー情報処理部 CalenderProcessクラス 担当: 角田 一颯

import requests
import uuid

class CalenderProcess:
    """
    カレンダー情報処理部
    タグ保存や削除の要求をC10 カレンダー情報管理部に送信する
    """

    def __init__(self, base_url="http://localhost:5001/api/calendar-manager"):
        """
        Args:
            base_url (str): 管理部APIのベースURL
        """
        self.base_url = base_url

    def tag_add(self, tag_name, tag_color, submitter_id, community_id, date):
        """
        M2 タグ追加処理（C10管理部に追加要求）

        Args:
            tag_name (str): 表示名
            tag_color (str): タグのカラーコード
            submmiter_id (str): 登録者のID
            community_id (str): コミュニティID
            date (Date): 対象の日付

        Returns:
            tuple[bool, dict]: (成功可否, 管理部からの応答内容)
        """
        
        #新規タグのIDをランダムに生成
        tag_id = uuid.uuid4()
        
        try:
            response = requests.post(
                f"{self.base_url}/tag/add",
                json={
                    "tag_id": tag_id,
                    "tag_name": tag_name,
                    "tag_color": tag_color,
                    "submitter_id": submitter_id,
                    "community_id": community_id,
                    "date": date
                    }
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json()
        except Exception as e:
            return False, {"error": "通信エラー", "details": str(e)}

    def tag_delete(self, tag_id):
        """
        M3 タグ削除処理（C10管理部に削除要求）

        Args:
            tag_id (str): タグID

        Returns:
            tuple[bool, dict]: (成功可否, 管理部からの応答内容)
        """
        try:
            response = requests.delete(
                f"{self.base_url}/tag/delete",
                json={
                      "tag_id": tag_id
                    }
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json()
        except Exception as e:
            return False, {"error": "通信エラー", "details": str(e)}

    def tag_get_from_community_and_date(self, community_id, date):
        """
        M4 タグコミュニティ検索処理
        
        Args:
            community_id (str): コミュニティID
            date (date)
        Returns:
            tuple[bool, dict]: (成功可否, 管理部からの応答内容)
        """
        try:
            response = requests.get(
                f"{self.base_url}/find/community/date",
                json={
                    "community_id": community_id,
                    "date": date
                    }
            )
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, response.json()
        except Exception as e:
            return False, {"error": "通信エラー", "details": str(e)}
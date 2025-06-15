# C7通知処理部の機能が実装されたNotificationクラスを定義するプログラム　作成者: 浅野勇翔

import os
from pathlib import Path
from dotenv import load_dotenv
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

class Notification:
    """
    C7 通知処理部
    """

    def __init__(self):
        """
        コンストラクタ
        LINEMessagingAPIとの接続を確立する
        """
        
        env_path = Path(__file__).parent
        load_dotenv(dotenv_path=env_path)
        self.__line_bot_api = LineBotApi(os.getenv('LINE_MESSAGING_API_ACCESS_TOKEN'))
        
    def send_match_message(self, user_ids, message):
        """
        指定されたユーザに指定されたメッセージをLINEMessagingAPIにより通知する
        
        Args:
            user_ids (list[str]): メッセージを通知するユーザのLINE IDのリスト
            message (str): 送信する文言
        
        Returns: 
            bool: 処理の成否(True=成功,False=失敗)
        """
        
        messages = TextSendMessage(text=message)
        
        try:
            for user_id in user_ids:
                self.__line_bot_api.push_message(user_id, messages=messages)
            return True
        except LineBotApiError as e:
            print(f"LINE送信エラー: {e}")
            return False
    
    
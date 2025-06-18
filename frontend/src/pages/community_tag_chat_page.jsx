import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';

/**
 * M23 タグチャット画面
 * 特定のタグに関連するチャットメッセージを表示し、ユーザーが新しいメッセージを送信できるようにする。
 *
 * 作成者: (TBD)
 */
const CommunityTagChatPage = () => {
  const { communityId, tagId } = useParams(); // URLからcommunityIdとtagIdを取得
  const query = new URLSearchParams(window.location.search);
  const date = query.get('date'); // クエリパラメータから日付を取得 
  const navigate = useNavigate();

  const [chatHistory, setChatHistory] = useState([]);
  const [chatMessage, setChatMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [postStatus, setPostStatus] = useState(""); // 

  const userId = Cookies.get('userId'); // 現在のユーザーIDを取得

  useEffect(() => {
    const fetchChatHistory = async () => {
      try {
        // チャット履歴を取得するAPIコール 
        const res = await axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/tag/${tagId}/chat?date=${date}`);
        setChatHistory(res.data.chat_history); // 
      } catch (err) {
        console.error("チャット履歴の取得に失敗しました: ", err);
        setError("チャット履歴の取得に失敗しました。"); // 
      } finally {
        setLoading(false);
      }
    };

    fetchChatHistory();
  }, [communityId, tagId, date]);

  const handleSendMessage = async () => {
    if (chatMessage.length > 200) { // 
      setError("半角英数字200文字以内で入力してください"); // 
      setPostStatus("メッセージの送信に失敗しました。"); // 
      return;
    }

    try {
      // チャットメッセージを送信するAPIコール 
      const res = await axios.post(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/tag/${tagId}/chat`, {
        date, // 
        message: chatMessage, // 
        sender_id: userId // 送信者のユーザーID
      });
      setChatHistory([...chatHistory, res.data.new_message]); // 送信成功後、履歴を更新 
      setChatMessage(""); // 入力欄をクリア
      setPostStatus("送信成功"); // 
    } catch (err) {
      console.error("メッセージの送信に失敗しました: ", err);
      setError("メッセージの送信に失敗しました。"); // 
      setPostStatus("メッセージの送信に失敗しました。"); // 
    }
  };

  const handleCloseClick = () => {
    // 日付ごとのタグ一覧画面 (W15/M22) に戻る 
    navigate(`/community/${communityId}/calendar/tags/${date}`);
  };

  if (loading) return <div className="p-4">読み込み中...</div>;

  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-white shadow-lg rounded-lg">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">タグチャット ({date})</h2>
        <button onClick={handleCloseClick} className="text-gray-500 hover:text-gray-700 text-xl font-bold">
          X
        </button>
      </div>

      {error && <p className="text-center text-red-500 mb-4">{error}</p>}
      {postStatus && <p className="text-center text-blue-500 mb-4">{postStatus}</p>}

      <div className="chat-history h-64 overflow-y-auto border p-4 rounded mb-4">
        {chatHistory.length > 0 ? (
          chatHistory.map((chat, index) => (
            <div key={index} className={`mb-2 ${chat.sender_id === userId ? 'text-right' : 'text-left'}`}>
              <span className="font-semibold">{chat.sender_name || 'Unknown'}: </span>
              <span>{chat.message_content}</span>
              <div className="text-xs text-gray-500">{new Date(chat.timestamp).toLocaleString()}</div>
            </div>
          ))
        ) : (
          <p className="text-gray-600">まだメッセージはありません。</p>
        )}
      </div>

      <div className="flex">
        <input
          type="text"
          value={chatMessage}
          onChange={(e) => setChatMessage(e.target.value)}
          placeholder="メッセージを入力..."
          className="flex-grow border rounded-l-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleSendMessage}
          className="px-4 py-2 bg-blue-500 text-white rounded-r-md hover:bg-blue-600"
        >
          送信
        </button>
      </div>
    </div>
  );
};

export default CommunityTagChatPage;

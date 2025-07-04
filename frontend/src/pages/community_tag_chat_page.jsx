import React, { useState, useEffect, useRef } from 'react'; // useRef を追加
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
  const { communityId, tagId } = useParams();
  const query = new URLSearchParams(window.location.search);
  const date = query.get('date');
  const navigate = useNavigate();

  const [chatHistory, setChatHistory] = useState([]);
  const [chatMessage, setChatMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [postStatus, setPostStatus] = useState("");

  const userId = Cookies.get('userId'); // 現在のユーザーIDを取得

  const chatHistoryRef = useRef(null); // チャット履歴のスクロール用Ref

  // リアルタイム性が必要な場合は、WebSocketなどを検討
  const fetchChatHistory = async () => {
    try {
      setError(""); // エラーをクリア
      const res = await axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/tag/${tagId}/chat/history?date=${date}`);
      // バックエンドが chat_history を配列で返すと仮定
      setChatHistory(res.data.chat_history || []);
    } catch (err) {
      console.error("チャット履歴の取得に失敗しました: ", err);
      setError("チャット履歴の取得に失敗しました。サーバーとの接続を確認してください。");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchChatHistory();

    // 読み込み後、チャット履歴を一番下までスクロール
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [communityId, tagId, date]); // 依存配列にcommunityId, tagId, dateを含める

  // 新しいメッセージが追加されたら自動でスクロール
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [chatHistory]);


  const handleSendMessage = async () => {
    // メッセージが空でないか、半角英数字200文字以内かチェック
    if (!chatMessage.trim()) { // 空白のみのメッセージも拒否
      setError("メッセージが未入力です。");
      setPostStatus("メッセージの送信に失敗しました。");
      return;
    }
    if (chatMessage.length > 200) {
      setError("メッセージは半角英数字200文字以内で入力してください。");
      setPostStatus("メッセージの送信に失敗しました。");
      return;
    }

    try {
      setError(""); // エラーをクリア
      setPostStatus("送信中..."); // 送信中ステータス
      const res = await axios.post(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/tag/${tagId}/chat/post`, {
        date,
        message: chatMessage,
        sender_id: userId
      });

      // バックエンドのレスポンス形式に依存
      // `CommunityManagement().post_chat` が新しいメッセージオブジェクトを返すことを想定
      if (res.data && res.data.new_message) {
        setChatHistory((prevHistory) => [...prevHistory, res.data.new_message]);
        setChatMessage(""); // 入力欄をクリア
        setPostStatus("送信成功！");
        // 数秒後にステータス表示を消す
        setTimeout(() => setPostStatus(""), 3000);
      } else {
        // バックエンドが新しいメッセージを返さない場合のフォールバック
        // 再度履歴をフェッチするか、エラーとする
        console.warn("サーバーが新しいメッセージデータを返しませんでした。履歴を再取得します。");
        fetchChatHistory(); // 履歴を再取得
        setChatMessage(""); // 入力欄をクリア
        setPostStatus("送信成功（履歴更新）");
        setTimeout(() => setPostStatus(""), 3000);
      }

    } catch (err) {
      console.error("メッセージの送信に失敗しました: ", err);
      // エラーメッセージをユーザーフレンドリーにする
      let errorMessage = "メッセージの送信に失敗しました。";
      if (err.response) {
        if (err.response.status === 400) {
          errorMessage = err.response.data.error || "無効なメッセージです。";
        } else if (err.response.status === 401 || err.response.status === 403) {
          errorMessage = "認証エラーです。ログインし直してください。";
        } else {
          errorMessage = "サーバーエラーが発生しました。";
        }
      }
      setError(errorMessage);
      setPostStatus("メッセージの送信に失敗しました。");
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

      <div ref={chatHistoryRef} className="chat-history h-64 overflow-y-auto border p-4 rounded mb-4">
        {chatHistory.length > 0 ? (
          chatHistory.map((chat, index) => (
            <div key={index} className={`mb-2 ${chat.sender_id === userId ? 'text-right' : 'text-left'}`}>
              {/* sender_name がない場合は、sender_id を表示するなど工夫が必要 */}
              <span className="font-semibold">{chat.sender_name || `User ID: ${chat.sender_id}`}: </span>
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

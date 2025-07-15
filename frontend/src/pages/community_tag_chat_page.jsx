import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';

/**
 * M23 タグチャット画面
 * 10秒ごとにチャット履歴を自動更新し、読み込み中インジケータをヘッダーに移動
 * 作成者:関太生
 */
const CommunityTagChatPage = () => {
  const { communityId, tagId } = useParams();
  const query = new URLSearchParams(window.location.search);
  const date = query.get('date');
  const navigate = useNavigate();

  const [chatHistory, setChatHistory] = useState([]);
  const [chatMessage, setChatMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [postStatus, setPostStatus] = useState('');

  const userId = Cookies.get('userId');
  const chatHistoryRef = useRef(null);

  // チャット履歴取得
  const fetchChatHistory = async () => {
    setLoading(true);
    try {
      setError('');
      const res = await axios.get(
        `${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/tag/${tagId}/chat/history?date=${date}`
      );
      setChatHistory(res.data.chat_history || []);
    } catch (err) {
      console.error('チャット履歴の取得に失敗しました: ', err);
      setError('チャット履歴の取得に失敗しました。サーバーとの接続を確認してください。');
    } finally {
      setLoading(false);
    }
  };

  // 初回とパラメーター変更時に履歴取得
  useEffect(() => {
    fetchChatHistory();
  }, [communityId, tagId, date]);

  // 10秒ごとに自動更新
  useEffect(() => {
    const interval = setInterval(fetchChatHistory, 10000);
    return () => clearInterval(interval);
  }, [communityId, tagId, date]);

  // 履歴更新時に自動スクロール
  useEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [chatHistory]);

  // メッセージ送信
  const handleSendMessage = async () => {
    if (!chatMessage.trim()) {
      setError('メッセージが未入力です。');
      return;
    }
    if (chatMessage.length > 200) {
      setError('メッセージは半角英数字200文字以内で入力してください。');
      return;
    }
    try {
      setError('');
      setPostStatus('送信中...');
      const userInfoRes = await axios.get(
        `${process.env.REACT_APP_API_SERVER_URL}/api/user/get/${userId}`
      );
      const userName = userInfoRes.data.user_data.name;
      const res = await axios.post(
        `${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/tag/${tagId}/chat/post`,
        { date, message: chatMessage, sender_id: userId, sender_name: userName }
      );
      if (res.data?.new_message) {
        setChatHistory(prev => [...prev, res.data.new_message]);
        setChatMessage('');
        setPostStatus('送信成功！');
        setTimeout(() => setPostStatus(''), 3000);
      } else {
        await fetchChatHistory();
        setChatMessage('');
        setPostStatus('送信成功（履歴更新）');
        setTimeout(() => setPostStatus(''), 3000);
      }
    } catch (err) {
      console.error('メッセージの送信に失敗しました: ', err);
      let msg = 'メッセージの送信に失敗しました。';
      if (err.response) {
        if (err.response.status === 400) msg = err.response.data.error || msg;
        else if ([401, 403].includes(err.response.status)) msg = '認証エラーです。ログインし直してください。';
      }
      setError(msg);
      setPostStatus('メッセージの送信に失敗しました。');
    }
  };

  const handleCloseClick = () => {
    navigate(`/community/${communityId}/calendar/tags/${date}`);
  };

  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-white shadow-lg rounded-lg">
      {/* ヘッダー */}
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center">
          <h2 className="text-2xl font-bold">タグチャット ({date})</h2>
          {loading && (
            <span className="ml-2 text-sm text-gray-500">読み込み中...</span>
          )}
        </div>
        <button
          onClick={handleCloseClick}
          className="text-gray-500 hover:text-gray-700 text-xl font-bold"
          title="閉じる"
        >
          X
        </button>
      </div>

      {error && <p className="text-center text-red-500 mb-4">{error}</p>}
      {postStatus && <p className="text-center text-blue-500 mb-4">{postStatus}</p>}

      {/* チャット履歴 */}
      <div
        ref={chatHistoryRef}
        className="chat-history h-64 overflow-y-auto border p-4 rounded mb-4"
      >
        {chatHistory.length > 0 ? (
          chatHistory.map((chat, idx) => (
            <div
              key={idx}
              className={`mb-2 ${chat.sender_id === userId ? 'text-right' : 'text-left'}`}
            >
              <span className="font-semibold">
                {chat.sender_name || `User ID: ${chat.sender_id}`}: 
              </span>
              <span>{chat.message_content || chat.message}</span>
              <div className="text-xs text-gray-500">
                {new Date(chat.timestamp).toLocaleString()}
              </div>
            </div>
          ))
        ) : (
          <p className="text-gray-600">まだメッセージはありません。</p>
        )}
      </div>

      {/* 入力エリア */}
      <div className="flex">
        <button
          onClick={fetchChatHistory}
          className="px-4 py-2 bg-gray-200 text-gray-700 border border-r-0 rounded-l-md hover:bg-gray-300"
          title="再読み込み"
        >
          🔄
        </button>
        <input
          type="text"
          value={chatMessage}
          onChange={e => setChatMessage(e.target.value)}
          placeholder="メッセージを入力..."
          className="flex-grow border-t border-b border-gray-300 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={handleSendMessage}
          className="px-4 py-2 bg-blue-500 text-white border border-l-0 rounded-r-md hover:bg-blue-600"
        >
          送信
        </button>
      </div>
    </div>
  );
};

export default CommunityTagChatPage;

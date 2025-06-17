import React from 'react';
import { useNavigate } from 'react-router-dom';
//import axios from 'axios';

const LogoutUI = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      // C2 にログアウトリクエストを送信
      //await axios.post('/api/logout'); // ←ここをC2のURLに変更する
      navigate('/login'); // ログアウト後にログイン画面などへ遷移
    } catch (error) {
      console.error('ログアウト失敗:', error);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-100 text-center px-4">
      <div className="bg-white p-6 rounded-lg shadow-md max-w-md w-full">
        <h2 className="text-xl font-semibold mb-4">ログアウトしますか？</h2>
        <div className="flex justify-center gap-6">
          <button
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            onClick={handleLogout}
          >
            はい
          </button>
          <button
            className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400"
            onClick={() => navigate(-1)} // 一つ前の画面に戻る
          >
            いいえ
          </button>
        </div>
      </div>
    </div>
  );
};

export default LogoutUI;

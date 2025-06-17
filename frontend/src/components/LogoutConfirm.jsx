/**
 * ログアウト確認画面
 * 「はい」でログアウトAPI (C2) にリクエストを送り、トップページへ遷移
 * 作成者: 石田めぐみ
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutConfirm = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await fetch('/api/logout', { method: 'POST' });
      if (response.ok) {
        navigate('/'); // トップページへ遷移（必要に応じて変更）
      } else {
        alert('ログアウトに失敗しました');
      }
    } catch (error) {
      console.error('ログアウトエラー:', error);
      alert('通信エラーが発生しました');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gray-50">
      <p className="text-xl font-semibold mb-6">ログアウトしますか？</p>
      <div className="flex space-x-6">
        <button
          className="px-6 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          onClick={handleLogout}
        >
          はい
        </button>
        <button
          className="px-6 py-2 bg-gray-300 rounded hover:bg-gray-400"
          onClick={() => navigate(-1)} // ひとつ前のページへ戻る
        >
          いいえ
        </button>
      </div>
    </div>
  );
};

export default LogoutConfirm;
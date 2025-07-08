import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaCamera } from 'react-icons/fa';
import axios from 'axios';
import Cookies from 'js-cookie'; // ← 追加

function CommunityJoin() {
  const [communityName, setCommunityName] = useState('');
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const [communityId, setCommnityId] = useState("");

  const navigate = useNavigate();

  const handleJoin = async (e) => {
    e.preventDefault();
    const userId = Cookies.get('userId'); // ← Cookieから取得
    if (!userId) {
      alert('ログイン情報が見つかりません');
      return;
    }

    try {
      const res = await axios.post(`${process.env.REACT_APP_API_SERVER_URL}/api/community/join`, {
        community_name: communityName,
        user_id: userId
      });
      console.log(res);
      setCommnityId(res.data.community_id);
      setShowSuccessModal(true);
    } catch (error) {
      alert(
        error.response?.data?.error ||
        error.response?.data?.message ||
        error.message ||
        'サーバエラーが発生しました'
      );
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-5">
      {showSuccessModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-lg relative min-w-[300px] text-center shadow-lg">
            <button
              onClick={() => navigate(`/community/${communityId}/calendar/view`)}
              className="absolute top-2 right-2 text-xl text-gray-500 hover:text-black"
            >
              ×
            </button>
            <h3 className="mt-4 text-lg font-semibold">参加完了</h3>
          </div>
        </div>
      )}

      <form
        onSubmit={handleJoin}
        className="bg-white p-8 rounded-lg shadow-md w-full max-w-md text-center"
      >
        <h2 className="text-2xl font-bold mb-6">コミュニティ参加</h2>

        <div className="w-20 h-20 rounded-full border-2 border-gray-300 flex items-center justify-center mx-auto mb-6 text-gray-500">
          <FaCamera size={28} />
        </div>

        <input
          type="text"
          placeholder="コミュニティ名"
          value={communityName}
          onChange={(e) => setCommunityName(e.target.value)}
          required
          className="w-full p-2 mb-5 border border-gray-300 rounded"
        />

        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded"
        >
          参加する
        </button>
      </form>
    </div>
  );
}

export default CommunityJoin;

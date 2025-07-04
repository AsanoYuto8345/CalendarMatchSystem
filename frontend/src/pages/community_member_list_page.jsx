// community_member_list.jsx

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';

/**
 * M24 メンバー画面
 * 所属するコミュニティのメンバー一覧を表示する。
 *
 * 作成者: (TBD)
 */
const CommunityMemberListPage = () => {
  const { communityId } = useParams(); // URLからcommunityIdを取得
  const navigate = useNavigate();
  const [memberList, setMemberList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchMemberList = async () => {
      try {
        // Step 1: コミュニティメンバーのuser_idリストを取得
        const res = await axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/members?community_id=${communityId}`);
        const userIds = res.data.members; // user_idのリストを想定

        // Step 2: 各user_idに対応するユーザー詳細情報を取得
        const detailedMembers = await Promise.all(
          userIds.map(async (userId) => {
            try {
              // C3 ユーザ情報処理部のM4 ユーザデータ取得処理のエンドポイントを呼び出し 
              const userRes = await axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/user/get/${userId}`);
              return userRes.data.user_data; // user_dataにはuser_id, name, icon_nameなどが含まれる想定
            } catch (userErr) {
              console.warn(`ユーザーID ${userId} の情報取得に失敗しました: `, userErr);
              return { user_id: userId, user_name: `不明なユーザー (${userId})`, user_icon_url: '/icons/default_user.png' }; // 失敗した場合のフォールバック
            }
          })
        );
        setMemberList(detailedMembers);
      } catch (err) {
        console.error("メンバー情報の取得に失敗しました: ", err);
        if (err.response && err.response.status === 404) {
          setError("コミュニティが見つかりません。");
        } else {
          setError("メンバー情報の取得に失敗しました。");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchMemberList();
  }, [communityId, navigate]);

  const handleCloseClick = () => {
    // W2 カレンダー画面 (community_calendar_view_page) に戻る
    navigate(`/community/${communityId}/calendar/view`);
  };

  if (loading) return <div className="p-4">読み込み中...</div>;

  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-white shadow-lg rounded-lg">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">メンバー一覧</h2>
        <button onClick={handleCloseClick} className="text-gray-500 hover:text-gray-700 text-xl font-bold">
          X
        </button>
      </div>

      {error && <p className="text-center text-red-500 mb-4">{error}</p>}

      {memberList.length > 0 ? (
        memberList.map((member, index) => (
          <div key={index} className="flex items-center bg-gray-100 p-3 rounded-md mb-2">
            {/* user_icon_url と user_name を表示 */}
            <img src={member.user_icon_url} alt={member.user_name} className="w-10 h-10 rounded-full mr-3" />
            <span className="text-lg">{member.user_name}</span>
          </div>
        ))
      ) : (
        <p className="text-gray-600">このコミュニティにはメンバーがいません。</p>
      )}
    </div>
  );
};

export default CommunityMemberListPage;

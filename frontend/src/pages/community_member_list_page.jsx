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
        const res = await axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/members`); // 
        setMemberList(res.data.members); // 
      } catch (err) {
        console.error("メンバー情報の取得に失敗しました: ", err);
        if (err.response && err.response.status === 404) {
          setError("コミュニティが見つかりません。"); // 
          // コミュニティ選択画面へ遷移 
          navigate('/community/select'); // 仮の遷移先。実際の画面遷移パスに修正してください。
        } else {
          setError("メンバー情報の取得に失敗しました。"); // 
        }
      } finally {
        setLoading(false);
      }
    };

    fetchMemberList();
  }, [communityId, navigate]);

  const handleCloseClick = () => {
    // W2 カレンダー画面 (community_calendar_view_page) に戻る 
    navigate('/community/calendar/view');
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

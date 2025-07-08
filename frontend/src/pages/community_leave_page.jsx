// M15 コミュニティ脱退画面 担当者: 浅野勇翔
import axios from 'axios';
import Cookies from 'js-cookie';
import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import CommunityLeave from '../components/CommunityLeave';

/**
 * コミュニティ脱退画面
 * - URL パラメータ communityId を受け取って API からコミュニティ名を取得
 * - 取得結果を <CommunityLeave> に props で渡す
 * 
 * 作成者: 浅野勇翔
 */
const CommunityLeavePage = () => {
  // URLパラメータからcommunityIdを取得
  const { communityId } = useParams();
  const [communityName, setCommunityName] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  const onAcceptClick = () => {
    // C4 コミュニティ処理部にコミュニティ脱退を依頼

    const userId = Cookies.get('userId');

    axios.delete(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/members/${userId}`)
    .then(res => {
      setMsg("脱退しました");
      navigate("/");
    })
    .catch(err => {
      setMsg("脱退処理に失敗しました");
      console.error(err);
    })
  }

  const onRejectClick = () => {
    // community_calnedar_view_pageに遷移

    navigate(`/community/${communityId}/calendar/view`);
  }

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/info_by_id?community_id=${communityId}`)
      .then(res => {
        console.log(res.data);
        setCommunityName(res.data.community_name); 
      })
      .catch(err => {
        console.error(err);
        setError("コミュニティ情報の取得に失敗しました");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [communityId]);

  if(loading) return <div className="p-4">読み込み中...</div>;
  if(error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <CommunityLeave communityName={communityName} onAcceptClick={onAcceptClick} onRejectClick={onRejectClick} msg={msg} />
  );
}

export default CommunityLeavePage;
// M15 コミュニティ脱退画面 担当者: 浅野勇翔
import axios from 'axios'
import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

import CommunityLeave from '../components/CommunityLeave'

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

  useEffect(() => {
    // 
    axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}`)
      .then(res => {
        setCommunityName(res.data.community_name)  
      })
      .catch(err => {
        console.error(err)
        setError("コミュニティ情報の取得に失敗しました")
      })
      .finally(() => {
        setLoading(false)
      });
  }, [communityId]);

  if(loading) return <div className="p-4">読み込み中...</div>;
  if(error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <CommunityLeave communityName={communityName} />
  );
}

export default CommunityLeavePage;
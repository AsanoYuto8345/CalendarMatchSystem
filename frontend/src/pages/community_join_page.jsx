// src/pages/community_join_page.jsx

/**
 * コミュニティ参加ページコンテナ
 * 作成者: 遠藤 信輝
 */

import CommunityJoin from '../components/CommunityJoin'

/**
 * CommunityJoinPage
 * コミュニティ参加用 UI コンポーネントを表示するページコンテナ
 */
const CommunityJoinPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-10">
      <CommunityJoin />
    </div>
  )
}

export default CommunityJoinPage

// src/pages/community_create_page.jsx

/**
 * コミュニティ作成画面ページ
 * 作成者: 遠藤 信輝
 */

import React from 'react'
import CommunityCreate from '../components/CommunityCreate'

/**
 * CommunityCreatePage
 * コミュニティ作成用の UI コンポーネントを表示するページコンテナ
 */
const CommunityCreatePage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-10">
      <CommunityCreate />
    </div>
  )
}

export default CommunityCreatePage

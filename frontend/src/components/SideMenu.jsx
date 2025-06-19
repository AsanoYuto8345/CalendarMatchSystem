/**
 * ハンバーガーコンポーネント
 * ナビゲーション用のリンク一覧を表示
 * 作成者: 石田めぐみ
 */

import { Link, useLocation } from 'react-router-dom'

const SideMenu = () => {
  const location = useLocation()

  const menuItems = [
    { label: 'マイページ', path: '/mypage' },
    { label: 'カレンダー', path: '/calendar' },
    { label: 'コミュニティ', path: '/community' },
    { label: 'ログアウト', path: '/auth/logout' }
  ]

  return (
    <aside className="w-64 h-screen bg-gray-100 p-4 shadow-md">
      <h2 className="text-xl font-bold mb-6">メニュー</h2>
      <nav className="flex flex-col space-y-3">
        {menuItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`px-4 py-2 rounded hover:bg-blue-100 ${
              location.pathname.startsWith(item.path)
                ? 'bg-blue-200 font-semibold'
                : ''
            }`}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  )
}

export default SideMenu

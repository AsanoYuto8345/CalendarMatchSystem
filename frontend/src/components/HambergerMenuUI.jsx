import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const HambergerMenuUI = ({ communities = [] }) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
    setUserMenuOpen(false);
  };

  const toggleUserMenu = () => setUserMenuOpen(!userMenuOpen);
  const handleCommunityClick = (id) => {
    navigate(`/community/${id}`);
    setMenuOpen(false); // コミュニティ選択後、メニューを閉じる
  };

  const menuItems = [
    { label: 'カレンダー', path: '/calendar' },
    { label: 'メンバー', path: '/members' },
    { label: 'テンプレートタグ一覧', path: '/tags' }
  ];

  return (
    <div className="relative">
      {/* ☰ トグルボタン */}
      <button
        className="fixed top-4 left-4 z-50 text-3xl bg-white px-2 py-1 rounded shadow"
        onClick={toggleMenu}
      >
        ☰
      </button>

      {menuOpen && (
        // オーバーレイの背景
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={toggleMenu} // 背景クリックでメニューを閉じる
        ></div>
      )}

      {/* メニューコンテナ (アニメーションを追加可能) */}
      <div
        className={`fixed top-0 left-0 h-screen bg-white shadow-lg z-50 transform transition-transform duration-300 ease-in-out
          ${menuOpen ? 'translate-x-0' : '-translate-x-full'}`} // メニューの表示/非表示を制御
      >
        <div className="flex h-full"> {/* h-full を追加して親の高さに合わせる */}
          {/* 左側：コミュニティ＋ユーザアイコン */}
          <div className="flex flex-col justify-between bg-gray-200 w-16 py-4">
            <div className="flex flex-col items-center space-y-4">
              {communities.map((comm) => (
                <button
                  key={comm.id}
                  title={comm.name}
                  onClick={() => handleCommunityClick(comm.id)}
                  className="focus:outline-none" // フォーカス時のアウトラインを削除
                >
                  <img
                    src={comm.iconUrl}
                    alt={comm.name}
                    className="w-8 h-8 rounded-full"
                  />
                </button>
              ))}
              <button
                onClick={() => {
                  navigate('/community/create');
                  setMenuOpen(false); // メニューを閉じる
                }}
                className="focus:outline-none"
              >
                <span className="text-xl font-bold">＋</span>
              </button>
            </div>

            <div className="flex flex-col items-center">
              <button onClick={toggleUserMenu} className="focus:outline-none">
                <img
                  src="/icons/user-icon.png"
                  alt="User"
                  className="w-8 h-8 rounded-full"
                />
              </button>

              {/* ユーザーメニューの表示位置を調整 */}
              {userMenuOpen && (
                <div className="absolute left-full bottom-4 bg-white shadow-md p-2 rounded space-y-2 z-40 ml-2"> {/* left-fullで右にずらす、ml-2で間隔を空ける */}
                  <button
                    className="block w-full text-left px-4 py-1 hover:bg-gray-100"
                    onClick={() => {
                      navigate('/auth/edit');
                      setMenuOpen(false); // メニューを閉じる
                    }}
                  >
                    ユーザ情報編集
                  </button>
                  <button
                    className="block w-full text-left px-4 py-1 hover:bg-gray-100"
                    onClick={() => {
                      navigate('/auth/logout');
                      setMenuOpen(false); // メニューを閉じる
                    }}
                  >
                    ログアウト
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* メインメニュー */}
          <div className="bg-white w-60 p-4"> {/* ここはshadow-lgはメニューコンテナに任せる */}
            <h2 className="text-xl font-bold mb-4">メニュー</h2>
            <nav className="flex flex-col space-y-3">
              {menuItems.map((item) => (
                <button
                  key={item.path}
                  onClick={() => {
                    navigate(item.path);
                    setMenuOpen(false); // メニューを閉じる
                  }}
                  className={`px-4 py-2 rounded text-left ${
                    location.pathname.startsWith(item.path)
                      ? 'bg-blue-200 font-semibold'
                      : 'hover:bg-blue-100'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HambergerMenuUI;
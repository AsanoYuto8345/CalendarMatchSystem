/**
 * ハンバーガメニューUIコンポーネント
 * ハンバーガーメニュー表示/非表示
 * 作成者: 石田めぐみ
 */

import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const HambergerMenuUI = ({ communities = [] }) => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false); // この状態を再利用
  const navigate = useNavigate();
  const location = useLocation();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
    setUserMenuOpen(false); // ハンバーガーメニューが閉じるとき、ユーザーメニューも閉じる
  };

  const toggleUserMenu = () => {
    setUserMenuOpen(!userMenuOpen); // ユーザーメニューの表示/非表示を切り替え
  };

  const handleCommunityClick = (id) => {
    navigate(`/community/${id}`);
    setMenuOpen(false); // コミュニティ選択後、メニューを閉じる
  };

  // メニュー項目クリック時の共通処理
  const handleMenuItemClick = (path) => {
    navigate(path);
    setMenuOpen(false); // メニューを閉じる
    setUserMenuOpen(false); // 念のためユーザーメニューも閉じる
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
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={toggleMenu}
        ></div>
      )}

      {/* メニュー全体 */}
      <div
        className={`fixed top-0 left-0 h-screen bg-white shadow-lg z-50 transform transition-transform duration-300 ease-in-out ${
          menuOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-full">
          {/* 左側：コミュニティ切り替え */}
          <div className="flex flex-col justify-between bg-gray-200 w-16 py-4">
            <div className="flex flex-col items-center space-y-4">
              {communities.map((comm) => (
                <button
                  key={comm.id}
                  title={comm.name}
                  onClick={() => handleCommunityClick(comm.id)}
                  className="focus:outline-none"
                >
                  <img
                    src={comm.iconUrl}
                    alt={comm.name}
                    className="w-8 h-8 rounded-full"
                  />
                </button>
              ))}
              <button
                onClick={() => handleMenuItemClick('/community/create')}
                className="focus:outline-none"
              >
                <span className="text-xl font-bold">＋</span>
              </button>
            </div>

            {/* ユーザーアイコン（クリック可能にする） */}
            <div className="flex flex-col items-center w-full px-2">
              <button onClick={toggleUserMenu} className="focus:outline-none">
                <img
                  src="/icons/user-icon.png"
                  alt="User"
                  className="w-8 h-8 rounded-full"
                />
              </button>
              {/* ここにはユーザーメニュー項目は直接置かない */}
            </div>
          </div>

          {/* メインメニュー */}
          <div className="bg-white w-60 p-4 flex flex-col justify-between">
            <div>
              <h2 className="text-xl font-bold mb-4">メニュー</h2>
              <nav className="flex flex-col space-y-3">
                {menuItems.map((item) => (
                  <button
                    key={item.path}
                    onClick={() => handleMenuItemClick(item.path)}
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

            {/* ユーザーメニュー項目（userMenuOpen の状態に依存して表示） */}
            {userMenuOpen && ( // userMenuOpen が true の場合のみ表示
              <div className="border-t pt-4 mt-4 space-y-2">
                <button
                  className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-base rounded"
                  onClick={() => handleMenuItemClick('/auth/edit')}
                >
                  ユーザ情報編集
                </button>
                <button
                  className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-base rounded"
                  onClick={() => handleMenuItemClick('/auth/logout')}
                >
                  ログアウト
                </button>
              </div>
            )}
            {/* userMenuOpen が false の場合、この div はレンダリングされない */}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HambergerMenuUI;
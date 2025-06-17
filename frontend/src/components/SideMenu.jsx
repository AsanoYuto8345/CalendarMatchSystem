/**
 * ハンバーガーメニュー表示・ユーザー操作メニュー表示
 * 作成者: 石田めぐみ
 */

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SideMenu = () => {
  const navigate = useNavigate();
  const [menuVisible, setMenuVisible] = useState(false);
  const [profileMenuVisible, setProfileMenuVisible] = useState(false);

  const handleNavigate = (path) => {
    navigate(path);
    setMenuVisible(false);
    setProfileMenuVisible(false);
  };

  return (
    <div className="relative">
      {/* ハンバーガーボタン */}
      <button
        className="text-3xl p-2"
        onClick={() => setMenuVisible(!menuVisible)}
      >
        ☰
      </button>

      {/* メニュー表示 */}
      {menuVisible && (
        <div className="absolute top-12 left-0 flex bg-white shadow-lg rounded-xl z-50">
          {/* メインメニュー */}
          <div className="p-4 space-y-3 border-r border-gray-200">
            <button className="block text-left" onClick={() => handleNavigate('/w2')}>カレンダー</button>
            <button className="block text-left" onClick={() => handleNavigate('/w18')}>メンバー</button>
            <button className="block text-left" onClick={() => handleNavigate('/w10')}>テンプレートタグ一覧</button>
          </div>

          {/* 左側のアイコンメニュー */}
          <div className="flex flex-col items-center bg-gray-100 w-16 py-4 space-y-4 rounded-r-xl">
            <button className="w-8 h-8 bg-gray-300 rounded-full" onClick={() => handleNavigate('/w2')} />
            <button className="w-8 h-8 bg-gray-300 rounded-full" onClick={() => handleNavigate('/w2')} />
            <button className="w-8 h-8 bg-gray-300 rounded-full" onClick={() => handleNavigate('/w2')} />
            <button className="w-8 h-8 bg-gray-300 rounded-full text-xl font-bold" onClick={() => handleNavigate('/w4')}>
              ＋
            </button>

            {/* プロフィールメニュー */}
            <div className="relative">
              <button
                className="w-8 h-8 bg-gray-500 rounded-full text-white"
                onClick={() => setProfileMenuVisible(!profileMenuVisible)}
              >
                👤
              </button>
              {profileMenuVisible && (
                <div className="absolute top-full right-0 mt-2 w-40 bg-white border border-gray-300 rounded-xl shadow-lg p-3 space-y-2 z-50">
                  <button className="block w-full text-left" onClick={() => handleNavigate('/w19')}>
                    ユーザ情報編集
                  </button>
                  <button className="block w-full text-left" onClick={() => handleNavigate('/w17')}>
                    ログアウト
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SideMenu;

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
    <div className="flex">
      {/* 右側のメニュー */}
      <div className="relative">
        <button
          className="text-3xl p-2"
          onClick={() => setMenuVisible(!menuVisible)}
        >
          ☰
        </button>
        {menuVisible && (
          <div className="absolute top-12 left-0 bg-white border shadow p-4 space-y-2">
            <button className="block" onClick={() => handleNavigate('/w2')}>カレンダー</button>
            <button className="block" onClick={() => handleNavigate('/w18')}>メンバー</button>
            <button className="block" onClick={() => handleNavigate('/w10')}>テンプレートタグ一覧</button>

            {/* 左側の丸いアイコン群 */}
            <div className="flex flex-col items-center bg-gray-100 w-12 py-4 space-y-4">
              <button className="w-8 h-8 bg-gray-300 rounded-full" onClick={() => handleNavigate('/w2')} />
              <button className="w-8 h-8 bg-gray-300 rounded-full" onClick={() => handleNavigate('/w2')} />
              <button className="w-8 h-8 bg-gray-300 rounded-full" onClick={() => handleNavigate('/w2')} />
              <button className="w-8 h-8 bg-gray-300 rounded-full text-xl font-bold" onClick={() => handleNavigate('/w4')}>＋</button>
              
              <div className="relative">
                <button
                  className="w-8 h-8 bg-gray-500 rounded-full text-white"
                  onClick={() => setProfileMenuVisible(!profileMenuVisible)}
                >
                  👤
                </button>
                {profileMenuVisible && (
                  <div className="absolute top-full right-0 mt-2 w-40 bg-white border border-gray-300 rounded-xl shadow-lg p-3 space-y-2 z-50 transition-all duration-200">
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
    </div>
  );
};

export default SideMenu;

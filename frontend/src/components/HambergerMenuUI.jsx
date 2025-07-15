// M8 HambergerMenuUI.jsx
// 担当：石田めぐみ

import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Cookies from 'js-cookie';
import axios from 'axios';

const HambergerMenuUI = ({ selectedCommunityId, setSelectedCommunityId }) => {
  const [userId, setUserId] = useState('');
  const [userInfo, setUserInfo] = useState({});
  const [communities, setCommunities] = useState([]);
  const [menuOpen, setMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [plusMenuOpen, setPlusMenuOpen] = useState(false);
  const [selectedCommunityName, setSelectedCommunityName] = useState("");

  const navigate = useNavigate();
  const location = useLocation();

  /* ------------------ ハンドラ ------------------ */
  const toggleMenu = () => {
    setMenuOpen((prev) => !prev);
    setUserMenuOpen(false);
    setPlusMenuOpen(false);
  };

  const toggleUserMenu = () => setUserMenuOpen((prev) => !prev);

  const togglePlusMenu = () => {
    setPlusMenuOpen((prev) => !prev);
    setUserMenuOpen(false);
  };

  const handleCommunityClick = (id, name) => {
    setSelectedCommunityId(id);
    setSelectedCommunityName(name);
    navigate(`/community/${id}/calendar/view`);
    setMenuOpen(false);
    setPlusMenuOpen(false);
  };

  const handleMenuItemClick = (path) => {
    navigate(path);
    setMenuOpen(false);
    setUserMenuOpen(false);
    setPlusMenuOpen(false);
  };

  /* ------------------ 初期データ取得 ------------------ */
  useEffect(() => {
    const uid = Cookies.get('userId');
    setUserId(uid);

    if (!uid) return;

    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/user/get/${uid}`)
      .then((res) => setUserInfo(res.data.user_data))
      .catch((e) => console.error(e));

    axios
      .get(
        `${process.env.REACT_APP_API_SERVER_URL}/api/community/joined?user_id=${uid}`
      )
      .then((res) => {
        const joined = res.data.communities || [];
        setCommunities(joined);
        const urlCidMatch = location.pathname.match(/^\/community\/([^/]+)\//);
        const cidFromUrl = urlCidMatch ? urlCidMatch[1] : '';

        let targetCid = '';   // 最終的に採用する ID
        let targetCname = '';   // 採用する名前

        if (cidFromUrl) {
          // URL に ID が含まれている ⇒ それを優先
          const m = joined.find((c) => String(c.id) === String(cidFromUrl));
          if (m) {
            targetCid = m.id;
            targetCname = m.name;
          }
        }

        // URL に無い or 該当コミュニティが見つからない場合は先頭を採用
        if (!targetCid && joined.length > 0) {
          targetCid = joined[0].id;
          targetCname = joined[0].name;
        }

        // state 反映（空ならリセット扱い）
        setSelectedCommunityId(targetCid);
        setSelectedCommunityName(targetCname);
        /* ========== ここまで ========== */
      })
      .catch((e) => console.error(e));



  }, [location.pathname]);


  /* ------------------ JSX ------------------ */
  return (
    <div className="relative">
      {/* ハンバーガーアイコン */}
      <button
        className="fixed top-4 left-4 z-50 text-3xl bg-white px-2 py-1 rounded shadow"
        onClick={toggleMenu}
      >
        ☰
      </button>

      {/* オーバーレイ */}
      {menuOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={toggleMenu}
        />
      )}

      {/* スライドメニュー */}
      <div
        className={`fixed top-0 left-0 h-screen bg-white shadow-lg z-50 transform transition-transform duration-300 ease-in-out ${menuOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
      >
        <div className="flex h-full">
          {/* ---------- 左：コミュニティ一覧 + ＋ ---------- */}
          <div className="flex flex-col justify-between bg-gray-200 w-16 py-4">
            <div className="flex flex-col items-center space-y-4 relative">
              {communities.map((comm) => (
                <button
                  key={comm.id}
                  title={comm.name}
                  onClick={() => handleCommunityClick(comm.id, comm.name)}
                  className="focus:outline-none"
                >
                  {comm.iconUrl ? (
                    /* ------------ 通常：画像がある ------------ */
                    <img
                      src={`${process.env.REACT_APP_API_SERVER_URL}/${comm.iconUrl}`}
                      alt={comm.name}
                      className="w-8 h-8 rounded-full object-cover"
                      onError={(e) => {
                        // 読み込み失敗時も頭文字フォールバック
                        e.target.onerror = null;
                        e.target.style.display = 'none';
                        const initial = (comm.name || '').trim().charAt(0).toUpperCase() || '?';
                        e.target.parentNode.insertAdjacentHTML(
                          'afterbegin',
                          `<div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">${initial}</div>`
                        );
                      }}
                    />
                  ) : (
                    /* ------------ フォールバック：頭文字 ------------ */
                    <div className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">
                      {(comm.name || '').trim().charAt(0).toUpperCase() || '?'}
                    </div>
                  )}
                </button>
              ))}

              {/* ＋ボタン */}
              <button onClick={togglePlusMenu} className="focus:outline-none">
                <span className="text-xl font-bold">＋</span>
              </button>

              {/* ＋メニュー */}
              {plusMenuOpen && (
                <div className="absolute left-full top-0 ml-2 flex flex-col bg-white shadow-md rounded w-24">
                  <button
                    onClick={() => handleMenuItemClick('/community/join')}
                    className="px-2 py-1 text-left text-sm hover:bg-gray-100"
                  >
                    参加
                  </button>
                  <button
                    onClick={() => handleMenuItemClick('/community/create')}
                    className="px-2 py-1 text-left text-sm hover:bg-gray-100"
                  >
                    作成
                  </button>
                </div>
              )}
            </div>

            {/* ユーザーアイコン */}
            <div className="flex flex-col items-center w-full px-2">
              <button onClick={toggleUserMenu} className="focus:outline-none">
                {userInfo.icon_name ? (
                  <img
                    src={`${process.env.REACT_APP_API_SERVER_URL}${userInfo.icon_name}`}
                    alt={userInfo.name || 'user'}
                    className="w-8 h-8 rounded-full object-cover"
                    onError={(e) => {
                      e.target.onerror = null;
                      e.target.style.display = 'none';
                      const initial =
                        (userInfo.name || '').trim().charAt(0).toUpperCase() ||
                        '?';
                      e.target.parentNode.insertAdjacentHTML(
                        'afterbegin',
                        `<div class="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">${initial}</div>`
                      );
                    }}
                  />
                ) : (
                  <div className="w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold">
                    {(userInfo.name || '').trim().charAt(0).toUpperCase() || '?'}
                  </div>
                )}
              </button>
            </div>
          </div>

          {/* ---------- 右：メインメニュー ---------- */}
          <div className="bg-white w-60 p-4 flex flex-col justify-between">
            <div>
              <h2 className="text-xl font-bold mb-4">メニュー</h2>


              {selectedCommunityName && (
                <p className="text-lg font-semibold text-gray-800 mt-2 mb-4">
                  {selectedCommunityName}
                </p>
              )}
              <nav className="flex flex-col space-y-3">
                <button
                  onClick={() =>
                    {
                      if(selectedCommunityId){
                        handleMenuItemClick(
                          `/community/${selectedCommunityId}/calendar/view`
                        )
                      }
                    }
                  }
                  className={`px-4 py-2 rounded text-left ${location.pathname ===
                    `/community/${selectedCommunityId}/calendar/view`
                    ? 'bg-blue-200 font-semibold'
                    : 'hover:bg-blue-100'
                    }`}
                >
                  カレンダー
                </button>

                <button
                  onClick={() =>
                    { 
                      if(selectedCommunityId){
                        handleMenuItemClick(
                          `/community/${selectedCommunityId}/members`
                        )
                      }
                    }
                  }
                  className={`px-4 py-2 rounded text-left ${location.pathname ===
                    `/community/${selectedCommunityId}/members`
                    ? 'bg-blue-200 font-semibold'
                    : 'hover:bg-blue-100'
                    }`}
                >
                  メンバー
                </button>

                <button
                  onClick={() =>
                  {
                    if(selectedCommunityId){
                      handleMenuItemClick(
                        `/community/${selectedCommunityId}/template_tag/view`
                      )
                    }
                  }
                  }
                  className={`px-4 py-2 rounded text-left ${location.pathname ===
                    `/community/${selectedCommunityId}/template_tag/view`
                    ? 'bg-blue-200 font-semibold'
                    : 'hover:bg-blue-100'
                    }`}
                >
                  テンプレートタグ一覧
                </button>

                {/* コミュニティ脱退 */}
                {selectedCommunityId && (
                  <button
                    onClick={() =>
                      handleMenuItemClick(
                        `/community/${selectedCommunityId}/leave`
                      )
                    }
                    className="px-4 py-2 rounded text-left hover:bg-red-100 text-red-600"
                  >
                    コミュニティ脱退
                  </button>
                )}
              </nav>
            </div>

            {/* ユーザーメニュー */}
            {userMenuOpen && (
              <div className="border-t pt-4 mt-4 space-y-2">
                <button
                  className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-base rounded"
                  onClick={() => handleMenuItemClick(`/user/${userId}/edit`)}
                >
                  ユーザ情報編集
                </button>

                <button
                  className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-base rounded"
                  onClick={() => handleMenuItemClick('/auth/login')}
                >
                  ログイン
                </button>

                <button
                  className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-base rounded"
                  onClick={() => handleMenuItemClick('/auth/logout')}
                >
                  ログアウト
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HambergerMenuUI;

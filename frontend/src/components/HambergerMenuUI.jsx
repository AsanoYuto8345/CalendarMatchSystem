// HambergerMenuUI.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Cookies from 'js-cookie';
import axios from 'axios';

const HambergerMenuUI = ({ selectedCommunityId, setSelectedCommunityId }) => {
  const [userId, setUserId] = useState("");
  const [userInfo, setUserInfo] = useState({});
  const [communities, setCommunities] = useState([]);
  const [menuOpen, setMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [plusMenuOpen, setPlusMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
    setUserMenuOpen(false);
    setPlusMenuOpen(false);
  };

  const toggleUserMenu = () => {
    setUserMenuOpen(!userMenuOpen);
  };

  const togglePlusMenu = () => {
    setPlusMenuOpen(!plusMenuOpen);
    setUserMenuOpen(false);
  };

  const handleCommunityClick = (id) => {
    setSelectedCommunityId(id);
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

  useEffect(() => {
    const uid = Cookies.get('userId');
    setUserId(uid);

    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/user/get/${uid}`)
      .then((res) => {
        setUserInfo(res.data.user_data);
      })
      .catch((e) => console.error(e));

    axios
      .get(
        `${process.env.REACT_APP_API_SERVER_URL}/api/community/joined?user_id=${uid}`
      )
      .then((res) => {
        const joined = res.data.communities || [];
        setCommunities(joined);
        if (joined.length > 0) {
          setSelectedCommunityId(joined[0].id);
        }
      })
      .catch((e) => console.error(e));
  }, []);

  return (
    <div className="relative">
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
        />
      )}

      <div
        className={`fixed top-0 left-0 h-screen bg-white shadow-lg z-50 transform transition-transform duration-300 ease-in-out ${
          menuOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-full">
          {/* サイドバー：コミュニティアイコン & プラスメニュー */}
          <div className="flex flex-col justify-between bg-gray-200 w-16 py-4">
            <div className="flex flex-col items-center space-y-4 relative">
              {communities.map((comm) => (
                <button
                  key={comm.id}
                  title={comm.name}
                  onClick={() => handleCommunityClick(comm.id)}
                  className="focus:outline-none"
                >
                  <img
                    src={
                      comm.iconUrl
                        ? `${process.env.REACT_APP_API_SERVER_URL}/${comm.iconUrl}`
                        : `${process.env.REACT_APP_API_SERVER_URL}/uploads/default_community_icon.png`
                    }
                    alt={comm.name}
                    className="w-8 h-8 rounded-full"
                  />
                </button>
              ))}

              {/* プラスボタン */}
              <button onClick={togglePlusMenu} className="focus:outline-none">
                <span className="text-xl font-bold">＋</span>
              </button>

              {/* プラスメニューをプラスボタン右に表示 */}
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

            <div className="flex flex-col items-center w-full px-2">
              <button onClick={toggleUserMenu} className="focus:outline-none">
                <img
                  src={`${process.env.REACT_APP_API_SERVER_URL}/uploads/${userInfo.icon_name}`}
                  alt="User"
                  className="w-8 h-8 rounded-full"
                />
              </button>
            </div>
          </div>

          {/* メインメニュー */}
          <div className="bg-white w-60 p-4 flex flex-col justify-between">
            <div>
              <h2 className="text-xl font-bold mb-4">メニュー</h2>
              <nav className="flex flex-col space-y-3">
                <button
                  onClick={() =>
                    handleMenuItemClick(
                      `/community/${selectedCommunityId}/calendar/view`
                    )
                  }
                  className={`px-4 py-2 rounded text-left ${
                    location.pathname ===
                    `/community/${selectedCommunityId}/calendar/view`
                      ? 'bg-blue-200 font-semibold'
                      : 'hover:bg-blue-100'
                  }`}
                >
                  カレンダー
                </button>
                <button
                  onClick={() =>
                    handleMenuItemClick(
                      `/community/${selectedCommunityId}/members`
                    )
                  }
                  className={`px-4 py-2 rounded text-left ${
                    location.pathname ===
                    `/community/${selectedCommunityId}/members`
                      ? 'bg-blue-200 font-semibold'
                      : 'hover:bg-blue-100'
                  }`}
                >
                  メンバー
                </button>
                <button
                  onClick={() =>
                    handleMenuItemClick(
                      `/community/${selectedCommunityId}/template_tag/view`
                    )
                  }
                  className={`px-4 py-2 rounded text-left ${
                    location.pathname ===
                    `/community/${selectedCommunityId}/template_tag/view`
                      ? 'bg-blue-200 font-semibold'
                      : 'hover:bg-blue-100'
                  }`}
                >
                  テンプレートタグ一覧
                </button>
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

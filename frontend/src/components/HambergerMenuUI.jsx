import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Cookies from 'js-cookie';
import axios from 'axios';

const HambergerMenuUI = ({ selectedCommunityId, setSelectedCommunityId }) => {
  const [userInfo, setUserInfo] = useState({});
  const [communities, setCommunities] = useState([]);
  const [menuOpen, setMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const toggleMenu = () => {
    setMenuOpen(!menuOpen);
    setUserMenuOpen(false);
  };

  const toggleUserMenu = () => {
    setUserMenuOpen(!userMenuOpen);
  };

  const handleCommunityClick = (id) => {
    setSelectedCommunityId(id);
    navigate(`/community/${id}/calendar/view`);
    setMenuOpen(false);
  };

  const handleMenuItemClick = (path) => {
    navigate(path);
    setMenuOpen(false);
    setUserMenuOpen(false);
  };

  useEffect(() => {
    const userId = Cookies.get('userId');

    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/user/get/${userId}`)
      .then((res) => {
        setUserInfo(res.data.user_data);
      })
      .catch((e) => console.error(e));

    axios
      .get(
        `${process.env.REACT_APP_API_SERVER_URL}/api/community/joined?user_id=${userId}`
      )
      .then((res) => {
        setCommunities(res.data.communities || []);
        if (res.data.communities && res.data.communities.length > 0) {
          setSelectedCommunityId(res.data.communities[0].id);
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

          <div className="bg-white w-60 p-4 flex flex-col justify-between">
            <div>
              <h2 className="text-xl font-bold mb-4">メニュー</h2>
              <nav className="flex flex-col space-y-3">
                <button
                  onClick={() => handleMenuItemClick(
                    `/community/${selectedCommunityId}/calendar/view`
                  )}
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
                  onClick={() => handleMenuItemClick(
                    `/community/${selectedCommunityId}/members`
                  )}
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
                  onClick={() => handleMenuItemClick(
                    `/community/${selectedCommunityId}/template_tag/view`
                  )}
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

            {userMenuOpen && (
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
          </div>
        </div>
      </div>
    </div>
  );
};

export default HambergerMenuUI;

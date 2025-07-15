/**
 * M8 ログアウトページ
 * - ユーザーのCookieを削除し、サーバーにログアウト処理を依頼する
 * 作成者: 石田めぐみ
 */

import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import axios from 'axios';

import LogoutUI from '../components/LogoutUI';

const AuthLogoutPage = () => {
  const navigate = useNavigate();

  const onAcceptClick = () => {
    const sid = Cookies.get('sid'); // セッションIDを取得

    axios
      .delete(`${process.env.REACT_APP_API_SERVER_URL}/api/auth/logout`, {
        data: { sid }, // DELETEリクエストのbodyにsidを含める
      })
      .then(() => {
        // CookieからセッションIDとユーザーIDを削除
        Cookies.remove('sid');
        Cookies.remove('userId');
        navigate('/auth/login'); // ログイン画面へ
      })
      .catch((error) => {
        console.error('ログアウトAPI失敗:', error);
        alert('ログアウト処理に失敗しました');
      });
  };

  const onRejectClick = () => {
    navigate('/');
  };

  return (
    <LogoutUI onAcceptClick={onAcceptClick} onRejectClick={onRejectClick} />
  );
};

export default AuthLogoutPage;

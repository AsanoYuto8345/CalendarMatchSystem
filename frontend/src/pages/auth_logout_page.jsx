/**
 * M8 ログアウトページ
 * - ユーザーのCookieを削除してログアウト処理を行う
 * 作成者: 石田めぐみ
 */

import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

import LogoutUI from '../components/LogoutUI';

const AuthLogoutPage = () => {
  const navigate = useNavigate();

  const onAcceptClick = () => {
    // CookieからユーザーIDを削除
    Cookies.remove('userId');

    // ログインページへ遷移
    navigate('/auth/login');
  };

  const onRejectClick = () => {
    // カレンダー画面に戻る
    navigate('/calendar');
  };

  return (
    <LogoutUI onAcceptClick={onAcceptClick} onRejectClick={onRejectClick} />
  );
};

export default AuthLogoutPage;
/**
 * M7 ログイン処理画面
 * - ユーザー認証を行い、ログイン成功時にトップページへ遷移
 * 作成者: 石田めぐみ
 */

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

import LoginUI from '../components/LoginUI';

const AuthLoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const navigate = useNavigate();

  const handleEmailChange = (e) => setEmail(e.target.value);
  const handlePasswordChange = (e) => setPassword(e.target.value);

  const handleLoginClick = () => {
    setErrorMsg('');

    axios.post(`${process.env.REACT_APP_API_SERVER_URL}/api/auth/login`, {
      email,
      pw: password // バックエンド側が pw を期待しているならここを pw にする
    })
      .then((res) => {
        // サーバーからのレスポンスに sid を期待
        const sid = res.data.sid;
        Cookies.set('sid', sid);

        // 必要なら userId なども保存（将来的に）
        // Cookies.set('userId', res.data.user_id);

        // トップページへ遷移
        navigate('/calendar');
      })
      .catch((err) => {
        console.error(err);
        setErrorMsg('ログインに失敗しました。メールアドレスまたはパスワードをご確認ください。');
      });
  };

  return (
    <LoginUI
      email={email}
      password={password}
      onEmailChange={handleEmailChange}
      onPasswordChange={handlePasswordChange}
      onLoginClick={handleLoginClick}
      errorMsg={errorMsg}
    />
  );
};

export default AuthLoginPage;

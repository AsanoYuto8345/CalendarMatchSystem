/**
 * M7 ログイン処理画面（バリデーション追加版）
 * - ユーザー認証を行い、ログイン成功時にトップページへ遷移
 * 作成者: 石田めぐみ
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';

import LoginUI from '../components/LoginUI';

const AuthLoginPage = () => {
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const navigate                = useNavigate();

  // 既にsidとuserIdがあれば、勝手にホームへリダイレクト
  useEffect(() => {
    const sid    = Cookies.get('sid');
    const userId = Cookies.get('userId');
    if (sid && userId) {
      navigate('/');
    }
  }, [navigate]);

  const handleEmailChange    = e => setEmail(e.target.value);
  const handlePasswordChange = e => setPassword(e.target.value);

  const handleLoginClick = () => {
    setErrorMsg('');

    // --- 🔒 クライアント側バリデーション ---
    if (!email || !password) {
      setErrorMsg('メールアドレスとパスワードを入力してください。');
      return;
    }

    const emailRegex = /^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$/;
    if (!emailRegex.test(email)) {
      setErrorMsg('メールアドレスの形式が不正です。');
      return;
    }

    const passwordRegex = /^[A-Za-z0-9]{1,20}$/;
    if (!passwordRegex.test(password)) {
      setErrorMsg('パスワードは半角英数字20文字以内で入力してください。');
      return;
    }

    // --- 🔐 API送信 ---
    axios.post(`${process.env.REACT_APP_API_SERVER_URL}/api/auth/login`, {
      email,
      pw: password
    })
    .then(res => {
      const sid    = res.data.sid;
      const userId = res.data.user_id;
      Cookies.set('sid', sid);
      Cookies.set('userId', userId);
      navigate('/');
    })
    .catch(err => {
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

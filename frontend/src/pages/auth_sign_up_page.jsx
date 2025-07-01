/**
 * M6 サインアップ処理ページ
 * - ユーザー登録APIにフォーム情報を送信
 * - 成功時にログインページへ遷移
 * 作成者: 石田めぐみ
 */

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import SignUpUI from '../components/SignupUI';

const AuthSignupPage = () => {
  const [msg, setMsg] = useState('');
  const navigate = useNavigate();

  const onSubmitClick = () => {
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;
    const displayName = document.querySelector('input[name="display_name"]').value;
    const iconFile = document.querySelector('input[name="icon_file"]').files[0];

    if (!email || !password || !displayName) {
      setMsg('すべての必須項目を入力してください。');
      return;
    }

    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    formData.append('display_name', displayName);
    if (iconFile) {
      formData.append('icon_file', iconFile);
    }

    // APIエンドポイント: POST /api/user/register に変更
    axios.post(`${process.env.REACT_APP_API_SERVER_URL}/api/user/register`, formData)
      .then(() => {
        setMsg('アカウントを作成しました');
        // サインインページへ遷移
        navigate('/auth/login');
      })
      .catch(() => {
        setMsg('作成に失敗しました。もう一度お試しください。');
      });
  };

  return <SignUpUI onSubmitClick={onSubmitClick} msg={msg} />;
};

export default AuthSignupPage;

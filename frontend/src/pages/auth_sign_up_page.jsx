/**
 * サインアップ処理ページ
 * 作成者: 石田めぐみ
 */

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import SignUpUI from '../components/SignupUI';

/**
 * auth_signup_page
 * - サインアップフォーム表示
 * - 入力情報をC1（ユーザ作成API）へ送信
 * - 結果メッセージを表示
 */
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

    axios.post(`${process.env.REACT_APP_API_SERVER_URL}/api/users`, formData)
      .then(() => {
        setMsg('アカウントを作成しました');
        navigate('/signin');
      })
      .catch(() => {
        setMsg('作成に失敗しました。もう一度お試しください。');
      });
  };

  return <SignUpUI onSubmitClick={onSubmitClick} msg={msg} />;
};

export default AuthSignupPage;

/**
 * M6 サインアップ処理ページ（修正版）
 * - バックエンド仕様に合わせて送信形式を修正
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

    // ファイル名（存在すれば）を使って送信、なければデフォルト
    const iconName = iconFile ? iconFile.name : "default_icon.png";

    const requestData = {
      email: email,
      password: password,
      name: displayName,
      icon_name: iconName,
    };

    axios.post(
      `${process.env.REACT_APP_API_SERVER_URL}/api/user/register`,
      requestData,
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )
    .then((response) => {
      setMsg('アカウントを作成しました');
      console.log('サインアップ成功:', response.data);
      navigate('/auth/login');
    })
    .catch((error) => {
      if (error.response) {
        console.error('サインアップ失敗:', error.response.data);
        setMsg(`作成に失敗しました: ${error.response.data.error || 'もう一度お試しください。'}`);
      } else if (error.request) {
        console.error('サインアップ失敗: サーバーからの応答がありません。');
        setMsg('作成に失敗しました: サーバーに接続できませんでした。');
      } else {
        console.error('サインアップ失敗:', error.message);
        setMsg('作成に失敗しました。もう一度お試しください。');
      }
    });
  };

  return <SignUpUI onSubmitClick={onSubmitClick} msg={msg} />;
};

export default AuthSignupPage;

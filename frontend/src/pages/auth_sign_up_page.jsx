/**
 * M6 サインアップ処理ページ（バリデーション強化版）
 * - バックエンド仕様に合わせて送信形式を修正
 * - クライアント側バリデーション追加（形式・文字数）
 */

import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

import SignUpUI from '../components/SignupUI';

const AuthSignupPage = () => {
  const [msg, setMsg] = useState('');
  const navigate = useNavigate();

  const onSubmitClick = () => {
    // DOMから直接値を取得
    const email = document.querySelector('input[name="email"]').value.trim();
    const password = document.querySelector('input[name="password"]').value;
    const displayName = document.querySelector('input[name="display_name"]').value.trim();
    const iconFile = document.querySelector('input[name="icon_file"]').files[0]; // Fileオブジェクトを取得

    // 必須入力チェック
    if (!email || !password || !displayName) {
      setMsg('すべての必須項目を入力してください。');
      return;
    }

    // メール形式チェック（簡易）
    const emailRegex = /^[\w.-]+@[\w.-]+\.[A-Za-z]{2,}$/;
    if (!emailRegex.test(email)) {
      setMsg('メールアドレスの形式が不正です。');
      return;
    }

    // パスワード：半角英数字、最大20文字
    const passwordRegex = /^[A-Za-z0-9]{1,20}$/;
    if (!passwordRegex.test(password)) {
      setMsg('パスワードは半角英数字20文字以内で入力してください。');
      return;
    }

    // 表示名の文字数チェック（日本語OK）
    if (displayName.length > 20) {
      setMsg('表示名は20文字以内で入力してください。');
      return;
    }

    // FormDataオブジェクトを生成
    // ファイルを送信するため、FormDataを使用します。
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password); // バックエンドは'password'を期待
    formData.append('name', displayName); // バックエンドは'name'を期待

    // アイコンファイルが存在する場合のみFormDataに追加
    // バックエンドは 'icon_file' というフィールド名を期待します。
    if (iconFile) {
      formData.append('icon_file', iconFile);
    }
    // icon_file が存在しない場合、バックエンドは 'default_icon.png' を内部で設定するため、
    // ここで 'icon_name' をFormDataに追加する必要はありません。

    axios.post(
      `${process.env.REACT_APP_API_SERVER_URL}/api/user/register`,
      formData, // JSONではなくFormDataを送信
      {
        headers: {
          'Content-Type': 'multipart/form-data', // ファイル送信のために必要
        },
      }
    )
    .then((response) => {
      setMsg('アカウントを作成しました');
      console.log('サインアップ成功:', response.data);
      // サインアップ成功後、ログインページへ遷移
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

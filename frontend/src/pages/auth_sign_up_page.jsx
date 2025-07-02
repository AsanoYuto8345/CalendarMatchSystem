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

    // アイコンファイルをBase64エンコードする処理
    const reader = new FileReader();
    reader.readAsDataURL(iconFile);

    reader.onload = () => {
      const base64Image = reader.result.split(',')[1]; // "data:image/png;base64,..." の "base64,..." 以降を取得

      // 送信するデータをJSONオブジェクトとして構築
      const requestData = {
        email: email,
        password: password,
        name: displayName,
        // Base64エンコードされた画像データを追加
        // ファイル名やMIMEタイプも必要であれば追加
        icon_data: base64Image,
        icon_filename: iconFile ? iconFile.name : null, // ファイル名も送る
        icon_mimetype: iconFile ? iconFile.type : null, // MIMEタイプも送る
      };

      // APIエンドポイント: POST /api/user/register (変更なし)
      // ヘッダーはJSONを送信するため 'Content-Type': 'application/json' を明示的に設定
      axios.post(
        `${process.env.REACT_APP_API_SERVER_URL}/api/user/register`,
        requestData, // FormDataではなくJSONデータを送信
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
          setMsg(`作成に失敗しました: ${error.response.data.message || 'もう一度お試しください。'}`);
        } else if (error.request) {
          console.error('サインアップ失敗: サーバーからの応答がありません。');
          setMsg('作成に失敗しました: サーバーに接続できませんでした。');
        } else {
          console.error('サインアップ失敗:', error.message);
          setMsg('作成に失敗しました。もう一度お試しください。');
        }
      });
    };

    reader.onerror = (error) => {
      console.error('アイコンファイルの読み込みエラー:', error);
      setMsg('アイコンファイルの読み込み中にエラーが発生しました。');
    };
  };

  return <SignUpUI onSubmitClick={onSubmitClick} msg={msg} />;
};

export default AuthSignupPage;
/**
 * ログインフォームのUI。ユーザー名とパスワードを入力し、ログインボタンで送信。
 * 作成者: 石田めぐみ
 */

import React, { useState } from 'react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const LoginUI = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    // TODO: API経由でログイン処理を実装
    console.log('ログイン処理中:', { username, password });
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="bg-white p-6 rounded-2xl shadow-md w-full max-w-sm">
        <h1 className="text-2xl font-bold mb-4 text-center">ログイン</h1>

        <label className="block mb-2 text-sm font-medium text-gray-700">ユーザー名</label>
        <Input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="user@example.com"
        />

        <label className="block mt-4 mb-2 text-sm font-medium text-gray-700">パスワード</label>
        <Input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="••••••••"
        />

        <Button className="mt-6 w-full" onClick={handleLogin}>
          ログイン
        </Button>
      </div>
    </div>
  );
};

export default LoginUI;

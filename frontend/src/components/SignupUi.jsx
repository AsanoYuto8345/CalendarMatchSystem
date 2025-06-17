/**
 * サインアップ画面UI
 * 作成者: 石田めぐみ
 */

import React from "react";

const SignupUI = () => {
  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-semibold mb-6">サインアップ</h2>

      {/* メールアドレス */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">メールアドレス</label>
        <input
          type="text"
          name="email"
          className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:border-blue-300"
          placeholder="メールアドレスを入力"
        />
        <small className="text-xs text-gray-500">半角英数（50文字以内）</small>
      </div>

      {/* パスワード */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">パスワード</label>
        <input
          type="password"
          name="pw"
          className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:border-blue-300"
          placeholder="パスワードを入力"
        />
        <small className="text-xs text-gray-500">半角英数（20文字以内）</small>
      </div>

      {/* 表示名 */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">表示名</label>
        <input
          type="text"
          name="name"
          className="w-full border rounded px-3 py-2 text-sm focus:outline-none focus:ring focus:border-blue-300"
          placeholder="表示名を入力"
        />
        <small className="text-xs text-gray-500">半角英数（20文字以内）</small>
      </div>

      {/* アイコン画像 */}
      <div className="mb-6">
        <label className="block text-sm font-medium mb-1">アイコン画像</label>
        <input
          type="file"
          name="icon_name"
          accept="image/*"
          className="text-sm"
        />
        <small className="text-xs text-gray-500">画像データ（サイズ制限あり）</small>
      </div>

      {/* サインアップボタン */}
      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition"
      >
        サインアップ
      </button>
    </div>
  );
};

export default SignupUI;

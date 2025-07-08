/**
 * サインアップ画面UIコンポーネント
 * 作成者: 石田めぐみ
 */

import React from 'react';

/**
 * SignUpUI
 * - サインアップ用フォーム
 * - ユーザ情報（メール、パスワード、表示名、アイコン画像）と送信ボタン
 *
 * @param {Function} onSubmitClick - サインアップ実行処理
 * @param {string} msg - 結果メッセージの表示
 */
const SignupUI = ({ onSubmitClick, msg }) => {
  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-bold text-center mb-4">サインアップ</h2>

      <div className="mb-4">
        {/* メールアドレスの修正: htmlForとidを追加 */}
        <label htmlFor="email" className="block text-sm font-medium mb-1">メールアドレス</label>
        <input
          type="email"
          name="email"
          id="email" // ★ここを追加
          maxLength={50}
          className="w-full px-3 py-2 border border-gray-300 rounded"
          placeholder="example@example.com"
          required
        />
        <small className="text-gray-500">半角英数（50文字以内）</small>
      </div>

      <div className="mb-4">
        {/* パスワードの修正: htmlForとidを追加 */}
        <label htmlFor="password" className="block text-sm font-medium mb-1">パスワード</label>
        <input
          type="password"
          name="password"
          id="password" // ★ここを追加
          pattern="[A-Za-z0-9]*"
          maxLength={20}
          className="w-full px-3 py-2 border border-gray-300 rounded"
          placeholder="パスワード"
          required
        />
        <small className="text-gray-500">半角英数（20文字以内）</small>
      </div>

      <div className="mb-4">
        {/* 表示名の修正: htmlForとidを追加 */}
        <label htmlFor="displayName" className="block text-sm font-medium mb-1">表示名</label>
        <input
          type="text"
          name="display_name"
          id="displayName" // ★ここを追加
          maxLength={20}
          className="w-full px-3 py-2 border border-gray-300 rounded"
          placeholder="表示名"
          required
        />
        <small className="text-gray-500">半角英数日本語（20文字以内）</small>
      </div>

      <div className="mb-6">
        {/* アイコン画像の修正: htmlForとidを追加 */}
        <label htmlFor="iconFile" className="block text-sm font-medium mb-1">アイコン画像</label>
        <input
          type="file"
          name="icon_file"
          id="iconFile" // ★ここを追加
          accept="image/*"
          className="block w-full"
        />
        <small className="text-gray-500">画像ファイルを選択してください</small>
      </div>

      <button
        className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded"
        onClick={onSubmitClick}
      >
        サインアップ
      </button>

      {msg && <div className="mt-4 text-center text-sm text-red-500">{msg}</div>}
    </div>
  );
};

export default SignupUI;
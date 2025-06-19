/**
 * ログインUIコンポーネント
 * 入力欄とログインボタンを表示
 * 作成者: 石田めぐみ
 */

import React from 'react'

/**
 * ログインUI
 * @param {string} email - メールアドレス入力値
 * @param {string} password - パスワード入力値
 * @param {function} onEmailChange - メールアドレス変更時のハンドラ
 * @param {function} onPasswordChange - パスワード変更時のハンドラ
 * @param {function} onLoginClick - ログインボタンクリック時の処理
 * @param {string} errorMsg - エラーメッセージ（任意）
 */
const LoginUI = ({
  email,
  password,
  onEmailChange,
  onPasswordChange,
  onLoginClick,
  errorMsg
}) => {
  return (
    <div className="max-w-md mx-auto mt-20 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold text-center mb-6">ログイン</h2>

      <div className="mb-4">
        <label className="block mb-1 font-semibold">メールアドレス</label>
        <input
          type="email"
          value={email}
          onChange={onEmailChange}
          className="w-full px-3 py-2 border rounded"
          placeholder="example@example.com"
        />
      </div>

      <div className="mb-4">
        <label className="block mb-1 font-semibold">パスワード</label>
        <input
          type="password"
          value={password}
          onChange={onPasswordChange}
          className="w-full px-3 py-2 border rounded"
          placeholder="********"
        />
      </div>

      {errorMsg && (
        <p className="text-red-500 text-sm mb-4">{errorMsg}</p>
      )}

      <button
        onClick={onLoginClick}
        className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded"
      >
        ログイン
      </button>
    </div>
  )
}

export default LoginUI
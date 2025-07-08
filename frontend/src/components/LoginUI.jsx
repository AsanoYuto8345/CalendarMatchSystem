/**
 * ログインUIコンポーネント
 * 入力欄とログインボタン + ホーム画面ボタンを表示
 * 作成者: 石田めぐみ（入力制限付き）
 */

import React from 'react'
import { useNavigate } from 'react-router-dom'

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
  const navigate = useNavigate()

  return (
    <div className="max-w-md mx-auto mt-20 p-6 bg-white rounded shadow">
      <h2 className="text-2xl font-bold text-center mb-6">ログイン</h2>

      <div className="mb-4">
        <label htmlFor="loginEmail" className="block mb-1 font-semibold">
          メールアドレス
        </label>
        <input
          type="email"
          id="loginEmail"
          value={email}
          onChange={onEmailChange}
          maxLength={50}
          required
          className="w-full px-3 py-2 border rounded"
          placeholder="example@example.com"
        />
      </div>

      <div className="mb-4">
        <label htmlFor="loginPassword" className="block mb-1 font-semibold">
          パスワード
        </label>
        <input
          type="password"
          id="loginPassword"
          value={password}
          onChange={onPasswordChange}
          pattern="[A-Za-z0-9]*"
          maxLength={20}
          required
          className="w-full px-3 py-2 border rounded"
          placeholder="********"
        />
        <small className="text-gray-500">半角英数字20文字以内</small>
      </div>

      {errorMsg && <p className="text-red-500 text-sm mb-4">{errorMsg}</p>}

      <button
        onClick={onLoginClick}
        className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded"
      >
        ログイン
      </button>

      <button
        onClick={() => navigate('/')}
        className="w-full mt-3 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded"
      >
        ホーム画面へ
      </button>
    </div>
  )
}

export default LoginUI

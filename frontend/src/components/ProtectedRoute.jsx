// src/components/ProtectedRoute.jsx
import React, { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import Cookies from 'js-cookie';
import axios from 'axios';

export default function ProtectedRoute({ children }) {
  const [checking, setChecking] = useState(true);
  const [authorized, setAuthorized] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const sid    = Cookies.get('sid');
    const userId = Cookies.get('userId');
    if (!sid || !userId) {
      setAuthorized(false);
      setChecking(false);
      return;
    }

    axios.post(
      `${process.env.REACT_APP_API_SERVER_URL}/api/sid/validate`,
      { user_id: userId, sid }
    )
    .then(res => {
      if (res.data.valid) {
        setAuthorized(true);
      } else {
        setAuthorized(false);
      }
    })
    .catch(() => {
      setAuthorized(false);
    })
    .finally(() => {
      setChecking(false);
    });
  }, [location.pathname]);

  // 認証チェック中はローディング表示
  if (checking) {
    return <div className="p-4 text-center">認証を確認しています…</div>;
  }

  // 認証NGならログイン画面へリダイレクト
  if (!authorized) {
    return <Navigate to="/auth/login" replace />;
  }

  // 認証OKなら本来の子コンポーネントを描画
  return <>{children}</>;
}

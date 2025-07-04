// M1 認証主処理に対応する。 User関連のルーティングを行う

import { Route } from 'react-router-dom';
import AuthLoginPage from '../pages/auth_login_page';
import AuthLogoutPage from '../pages/auth_logout_page';
import AuthSignupPage from '../pages/auth_sign_up_page';

export const AuthRoutes = (
  <>
    <Route path="auth/login" element={<AuthLoginPage />} />
    <Route path="auth/logout" element={<AuthLogoutPage />} />
    <Route path="auth/signup" element={<AuthSignupPage />} />
  </>
)
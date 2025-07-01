// M3 ユーザUI主処理に対応する。 User関連のルーティングを行う

import { Route } from 'react-router-dom';

import UserInfoEditMPage from '../pages/user_info_edit_complete_page';
import UserInfoEditPage from '../pages/user_info_edit_page';

export const UserRoutes = (
  <>
    <Route path="/user/:userId/edit/complete" element={<UserInfoEditMPage />} />
    <Route path="/user/:userId/edit" element={<UserInfoEditPage />} />
  </>
)
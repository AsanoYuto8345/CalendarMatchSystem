// M3 ユーザUI主処理に対応する。 User関連のルーティングを行う

import { Route } from 'react-router-dom';
import UserInfoEditPage from '../pages/user_info_edit_page';

export const UserRoutes = (
  <>
    <Route path="/user/:userId/edit" element={<UserInfoEditPage />} />
  </>
)
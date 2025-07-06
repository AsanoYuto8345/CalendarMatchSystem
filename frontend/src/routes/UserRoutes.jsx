import React from 'react';
import { Route } from 'react-router-dom';
import ProtectedRoute from '../components/ProtectedRoute';

import UserInfoEditMPage from '../pages/user_info_edit_complete_page';
import UserInfoEditPage from '../pages/user_info_edit_page';

/**
 * M3 ユーザUI主処理に対応する。
 * User関連のルーティングを行う
 */
export const UserRoutes = [
  <Route
    key="user-edit"
    path="/user/:userId/edit"
    element={
      <ProtectedRoute>
        <UserInfoEditPage />
      </ProtectedRoute>
    }
  />,
  <Route
    key="user-edit-complete"
    path="/user/:userId/edit/complete"
    element={
      <ProtectedRoute>
        <UserInfoEditMPage />
      </ProtectedRoute>
    }
  />
];

// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う

import { Route } from 'react-router-dom';

import CommunityLeavePage from '../pages/community_leave_page'
import CommunityCreatePage from '../pages/community_create_page'
import CommunityJoinPage from '../pages/community_join_page' 

export const CommunityRoutes = (
  <>
      <Route path="community/:communityId/leave" element={<CommunityLeavePage />} />
      <Route path="/community/create" element={<CommunityCreatePage />} />
      <Route path="/community/join" element={<CommunityJoinPage />} />
  </>
)
// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う

import { Route } from 'react-router-dom';

import CommunityLeavePage from '../pages/community_leave_page';
import TemplateTagViewPage from '../pages/community_template_tag_view_page';
import TemplateTagEditPage from '../pages/community_template_tag_edit_page';
import TemplateTagCreatePage from '../pages/community_template_tag_create_page';
import CommunityCreatePage from '../pages/community_create_page'
import CommunityJoinPage from '../pages/community_join_page' 

export const CommunityRoutes = (
  <>
    <Route path="community/:communityId/leave" element={<CommunityLeavePage />} />
    <Route path="community/:communityId/template_tag/view" element={<TemplateTagViewPage />} />
    <Route path="community/:communityId/calendar/template_tag/:tagId/edit" element={<TemplateTagEditPage />} />
    <Route path="community/:communityId/calendar/template_tag/create" element={<TemplateTagCreatePage />} />
    <Route path="/community/create" element={<CommunityCreatePage />} />
    <Route path="/community/join" element={<CommunityJoinPage />} />
  </>
)
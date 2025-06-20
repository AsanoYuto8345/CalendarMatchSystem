// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う

import { Route } from 'react-router-dom';
import CommunityLeavePage from '../pages/community_leave_page';
import TemplateTagEditPage from '../pages/community_template_tag_edit_page';

export const CommunityRoutes = (
  <>
    <Route path="community/:communityId/leave" element={<CommunityLeavePage />} />
    <Route path="community/:communityId/calendar/template_tag/:tagId/edit" element={<TemplateTagEditPage />} />
  </>
)
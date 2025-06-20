// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う

import { Route } from 'react-router-dom';
import CommunityLeavePage from '../pages/community_leave_page';
import TemplateTagViewPage from '../pages/community_template_tag_view_page';

export const CommunityRoutes = (
  <>
    <Route path="community/:communityId/leave" element={<CommunityLeavePage />} />
    <Route path="community/:communityId/template_tag/view" element={<TemplateTagViewPage />} />
  </>
);
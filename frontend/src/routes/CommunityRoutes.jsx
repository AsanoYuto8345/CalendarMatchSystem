// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う

import { Route } from 'react-router-dom';
import CommunityLeavePage from '../pages/community_leave_page' 
import TagPostPage from '../pages/community_calendar_tag_post_page';
import TagPostCompleteMessagePage from '../pages/community_calendar_tag_post_complete_page';
import TagEditPage from '../pages/community_calendar_tag_edit_page';
import TagEditCompleteMesaagePage from '../pages/community_calendar_tag_edit_complete_page';

export const CommunityRoutes = (
  <>
    <Route path="community/:communityId/leave" element={<CommunityLeavePage />} />
    <Route path="community/:communityId/calendar/:date/tags/post" element={<TagPostPage />} />
    <Route path="community/:communityId/calendar/:date/tags/post/complate" element={<TagPostCompleteMessagePage />} />
    <Route path="community/:communityId/calendar/:date/tags/edit" element={<TagEditPage />} />
    <Route path="community/:communityId/calendar/:date/tags/edit/complate" element={<TagEditCompleteMesaagePage />} />
  </>
)
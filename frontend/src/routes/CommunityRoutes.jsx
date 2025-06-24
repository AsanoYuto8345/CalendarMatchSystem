// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う

import { Route } from 'react-router-dom';
import CommunityLeavePage from '../pages/community_leave_page' 
import CommunityCalendarViewPage from '../pages/community_calendar_view_page';

export const CommunityRoutes = (
  <>
    <Route path="community/:communityId/leave" element={<CommunityLeavePage />}/>
    <Route path="community/:communityId/calendar/view" element={<CommunityCalendarViewPage/>}/>
  </>
)
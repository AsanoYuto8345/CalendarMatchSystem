// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う

import { Route } from 'react-router-dom';
import CommunityLeavePage from '../pages/community_leave_page' 

import CommunityCalendarTagViewPage from '../pages/community_calendar_tag_view_page'; // M22
import CommunityTagChatPage from '../pages/community_tag_chat_page'; // M23
import CommunityMemberListPage from '../pages/community_member_list_page'; // M24

export const CommunityRoutes = (
  <>
    <Route path="community/:communityId/leave" element={<CommunityLeavePage />} />

    {/* M22 日付ごとのタグ一覧画面 */}
    <Route path="community/:communityId/calendar/tags/:date" element={<CommunityCalendarTagViewPage />} />
    {/* M23 タグチャット画面 */}
    <Route path="community/:communityId/tag/:tagId/chat" element={<CommunityTagChatPage />} />
    {/* M24 メンバー画面 */}
    <Route path="community/:communityId/members" element={<CommunityMemberListPage />} />
  </>
)


// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う 

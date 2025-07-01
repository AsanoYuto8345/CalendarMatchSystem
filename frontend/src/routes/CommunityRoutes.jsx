// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う

import { Route } from 'react-router-dom';

import CommunityLeavePage from '../pages/community_leave_page';
import TemplateTagViewPage from '../pages/community_template_tag_view_page';
import TemplateTagEditPage from '../pages/community_template_tag_edit_page';
import TemplateTagCreatePage from '../pages/community_template_tag_create_page';
import CommunityCreatePage from '../pages/community_create_page'
import CommunityJoinPage from '../pages/community_join_page' 
import TagPostPage from '../pages/community_calendar_tag_post_page';
import TagPostCompleteMessagePage from '../pages/community_calendar_tag_post_complete_page';
import TagEditPage from '../pages/community_calendar_tag_edit_page';
import TagEditCompleteMesaagePage from '../pages/community_calendar_tag_edit_complete_page';
import CommunityCalendarViewPage from '../pages/community_calendar_view_page';
import CommunityCalendarTagViewPage from '../pages/community_calendar_tag_view_page'; // M22
import CommunityTagChatPage from '../pages/community_tag_chat_page'; // M23
import CommunityMemberListPage from '../pages/community_member_list_page'; // M24

export const CommunityRoutes = (
  <>
    <Route path="community/:communityId/leave" element={<CommunityLeavePage />} />
    <Route path="community/:communityId/template_tag/view" element={<TemplateTagViewPage />} />
    <Route path="community/:communityId/calendar/template_tag/:tagId/edit" element={<TemplateTagEditPage />} />
    <Route path="community/:communityId/calendar/template_tag/create" element={<TemplateTagCreatePage />} />
    <Route path="/community/create" element={<CommunityCreatePage />} />
    <Route path="/community/join" element={<CommunityJoinPage />} />
    <Route path="community/:communityId/calendar/:date/tags/post" element={<TagPostPage />} />
    <Route path="community/:communityId/calendar/:date/tags/post/complate" element={<TagPostCompleteMessagePage />} />
    <Route path="community/:communityId/calendar/:date/tags/edit" element={<TagEditPage />} />
    <Route path="community/:communityId/calendar/:date/tags/edit/complate" element={<TagEditCompleteMesaagePage />} />
    {/* M22 日付ごとのタグ一覧画面 */}
    <Route path="community/:communityId/calendar/tags/:date" element={<CommunityCalendarTagViewPage />} />
    {/* M23 タグチャット画面 */}
    <Route path="community/:communityId/tag/:tagId/chat" element={<CommunityTagChatPage />} />
    {/* M24 メンバー画面 */}
    <Route path="community/:communityId/members" element={<CommunityMemberListPage />} />
    <Route path="community/:communityId/leave" element={<CommunityLeavePage />}/>
    <Route path="community/:communityId/calendar/view" element={<CommunityCalendarViewPage/>}/>
  </>
)


// M4 コミュニティUI主処理に対応する。 Community関連のルーティングを行う 

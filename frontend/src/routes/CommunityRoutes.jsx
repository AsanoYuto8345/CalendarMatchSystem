import React from 'react';
import { Route } from 'react-router-dom';
import ProtectedRoute from '../components/ProtectedRoute';

import CommunityLeavePage from '../pages/community_leave_page';
import TemplateTagViewPage from '../pages/community_template_tag_view_page';
import TemplateTagEditPage from '../pages/community_template_tag_edit_page';
import TemplateTagCreatePage from '../pages/community_template_tag_create_page';
import CommunityCreatePage from '../pages/community_create_page';
import CommunityJoinPage from '../pages/community_join_page';
import TagPostPage from '../pages/community_calendar_tag_post_page';
import TagPostCompleteMessagePage from '../pages/community_calendar_tag_post_complete_page';
import TagEditPage from '../pages/community_calendar_tag_edit_page';
import TagEditCompleteMessagePage from '../pages/community_calendar_tag_edit_complete_page';
import CommunityCalendarViewPage from '../pages/community_calendar_view_page';
import CommunityCalendarTagViewPage from '../pages/community_calendar_tag_view_page';
import CommunityTagChatPage from '../pages/community_tag_chat_page';
import CommunityMemberListPage from '../pages/community_member_list_page';

/**
 * M4 コミュニティUI主処理に対応する。
 * Community関連のルーティングを行う
 */
export const CommunityRoutes = [
  <Route
    key="community-leave"
    path="/community/:communityId/leave"
    element={
      <ProtectedRoute>
        <CommunityLeavePage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="template-tag-view"
    path="/community/:communityId/template_tag/view"
    element={
      <ProtectedRoute>
        <TemplateTagViewPage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="template-tag-edit"
    path="/community/:communityId/calendar/template_tag/:tagId/edit"
    element={
      <ProtectedRoute>
        <TemplateTagEditPage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="template-tag-create"
    path="/community/:communityId/calendar/template_tag/create"
    element={
      <ProtectedRoute>
        <TemplateTagCreatePage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="community-create"
    path="/community/create"
    element={
      <ProtectedRoute>
        <CommunityCreatePage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="community-join"
    path="/community/join"
    element={
      <ProtectedRoute>
        <CommunityJoinPage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="tag-post"
    path="/community/:communityId/calendar/:date/tags/post"
    element={
      <ProtectedRoute>
        <TagPostPage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="tag-post-complete"
    path="/community/:communityId/calendar/:date/tags/post/complate"
    element={
      <ProtectedRoute>
        <TagPostCompleteMessagePage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="tag-edit"
    path="/community/:communityId/calendar/:date/tags/edit"
    element={
      <ProtectedRoute>
        <TagEditPage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="tag-edit-complete"
    path="/community/:communityId/calendar/:date/tags/edit/complate"
    element={
      <ProtectedRoute>
        <TagEditCompleteMessagePage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="calendar-tag-view"
    path="/community/:communityId/calendar/tags/:date"
    element={
      <ProtectedRoute>
        <CommunityCalendarTagViewPage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="tag-chat"
    path="/community/:communityId/tag/:tagId/chat"
    element={
      <ProtectedRoute>
        <CommunityTagChatPage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="member-list"
    path="/community/:communityId/members"
    element={
      <ProtectedRoute>
        <CommunityMemberListPage />
      </ProtectedRoute>
    }
  />,  
  <Route
    key="calendar-view"
    path="/community/:communityId/calendar/view"
    element={
      <ProtectedRoute>
        <CommunityCalendarViewPage />
      </ProtectedRoute>
    }
  />
];

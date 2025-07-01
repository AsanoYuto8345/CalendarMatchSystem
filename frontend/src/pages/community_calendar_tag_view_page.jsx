import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import TagListViewByDate from '../components/TagListViewByDate';

/**
 * M22 日付ごとのタグ一覧画面
 * 特定の日付に投稿されたタグと、そのタグを投稿したコミュニティ内のメンバー一覧を表示する。
 *
 * 作成者: (TBD)
 */
const CommunityCalendarTagViewPage = () => {
  const { communityId, date } = useParams();
  const navigate = useNavigate();
  const [tagList, setTagList] = useState([]);
  const [memberList, setMemberList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTagAndMemberData = async () => {
      try {
        // 日付形式の検証 (例: YYYY-MM-DD)
        if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
          setError("日付の指定が不正です。");
          navigate('/community/calendar/view');
          return;
        }

        const tagRes = await axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/tags?date=${date}`);
        setTagList(tagRes.data.tags);

        const memberRes = await axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/members?date=${date}`);
        setMemberList(memberRes.data.members);

        if (tagRes.data.tags.length === 0 && memberRes.data.members.length === 0) {
          setError("この日付にはタグがありません。");
        }

      } catch (err) {
        console.error("情報の取得に失敗しました: ", err);
        setError("情報の取得に失敗しました。");
        if (err.response && err.response.status === 404) {
          setError("この日付にはタグがありません。");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchTagAndMemberData();
  }, [communityId, date, navigate]);

  const handleTagClick = (tagId) => {
    // M23 タグチャット画面 (community_tag_chat_page) へ遷移
    navigate(`/community/${communityId}/tag/${tagId}/chat?date=${date}`);
  };

  const handleEditClick = () => {
    // W13/M20 タグ編集画面 (community_calendar_tag_edit_page) へ遷移
    navigate(`/community/${communityId}/tag/edit?date=${date}`);
  };

  const handleAddTagClick = () => {
    // W11/M18 新規タグ入力画面 (community_calendar_tag_post_page) へ遷移
    navigate(`/community/${communityId}/tag/add?date=${date}`);
  };

  const handleCloseClick = () => {
    // W2 カレンダー画面 (community_calendar_view_page) に戻る
    navigate('/community/calendar/view');
  };

  if (loading) return <div className="p-4">読み込み中...</div>;

  return (
    <TagListViewByDate
      date={date}
      tagList={tagList}
      memberList={memberList}
      onTagClick={handleTagClick}
      onEditClick={handleEditClick}
      onAddTagClick={handleAddTagClick}
      onCloseClick={handleCloseClick}
      message={error}
    />
  );
};

export default CommunityCalendarTagViewPage;

// community_calendar_tag_view_page.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import TagListViewByDate from '../components/TagListViewByDate';

/**
 * M22 日付ごとのタグ一覧画面
 * 特定の日付に投稿されたタグと、そのタグを投稿したコミュニティ内のメンバー一覧を表示する。
 *
 * 作成者:関太生
 */
const CommunityCalendarTagViewPage = () => {
  const { communityId, date } = useParams();
  const navigate = useNavigate();
  const [tagList, setTagList] = useState([]);

  // メンバーリストは不要になったため削除
  // const [memberList, setMemberList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchTagData = async () => { // 関数名を fetchTagAndMemberData から fetchTagData に変更
      try {
        // 日付形式の検証 (例:YYYY-MM-DD)
        if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) {
          setError("日付の指定が不正です。");
          //navigate('/community/calendar/view');
          return;
        }

        // C4 カレンダー情報処理部 M4 タグコミュニティ検索処理からタグリストを取得
        const tagRes = await axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/${communityId}/calendar/tag/get?date=${date}`);
        const fetchedTags = tagRes.data.data || [];
        console.log(fetchedTags);

        if (fetchedTags.length === 0) {
          setError("この日付にはタグがありません。");
          setTagList([]);
          // setMemberList([]); // メンバーリストのクリアも不要
          setLoading(false);
          return;
        }

        // メンバーに関する処理を全て削除
        // // タグを投稿したユーザーIDの重複を排除してリスト化
        // const uniqueSubmitterIds = [...new Set(fetchedTags.map(tag => tag.submitter_id))];

        // // 各submitter_idに対してC8 ユーザ情報管理部 M2 の user_data_search を呼び出し、ユーザー名を取得
        // const userPromises = uniqueSubmitterIds.map(async (userId) => {
        //   try {
        //     // C8 ユーザ情報管理部 M2 ユーザ情報検索処理のエンドポイントは /api/users/search で、クエリパラメータ 'id' を使用
        //     const userRes = await axios.get(`${process.env.REACT_APP_API_SERVER_URL}/api/users/search`, {
        //       params: { id: userId }
        //     });
        //     return userRes.data; // ユーザーデータにはid, name, email, iconなどが含まれると想定
        //   } catch (userErr) {
        //     console.error(`ユーザー情報取得失敗 for ID ${userId}: `, userErr);
        //     return null; // 取得失敗した場合はnullを返す
        //   }
        // });

        // const usersData = await Promise.all(userPromises);
        // // 取得できたユーザーデータのみをフィルタリングし、memberListを構築
        // const validUsers = usersData.filter(user => user !== null);
        // setMemberList(validUsers.map(user => ({ user_id: user.id, user_name: user.name, user_icon_url: user.icon })));

        // // タグリストにユーザー名を付与
        // const tagsWithSubmitterNames = fetchedTags.map(tag => {
        //   const submitter = validUsers.find(user => user.id === tag.submitter_id);
        //   return {
        //     ...tag,
        //     submitter_name: submitter ? submitter.name : '不明なユーザー'
        //   };
        // });
        // setTagList(tagsWithSubmitterNames); // メンバー情報を付与しないタグリストをセット

        // 単純に取得したタグリストをセットする
        setTagList(fetchedTags);

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

    fetchTagData(); // 関数名を変更
  }, [communityId, date, navigate]);

  const handleTagClick = (tagId) => {
    // M23 タグチャット画面 (community_tag_chat_page) へ遷移
    navigate(`/community/${communityId}/tag/${tagId}/chat?date=${date}`);
  };

  const handleEditClick = () => {
    // W13/M20 タグ編集画面 (community_calendar_tag_edit_page) へ遷移
    navigate(`/community/${communityId}/calendar/${date}/tags/edit`);
  };

  const handleAddTagClick = () => {
    // W11/M18 新規タグ入力画面 (community_calendar_tag_post_page) へ遷移
    navigate(`/community/${communityId}/calendar/${date}/tags/post`);
  };

  const handleCloseClick = () => {
    // W2 カレンダー画面 (community_calendar_view_page) に戻る
    navigate(`/community/${communityId}/calendar/view`);
  };

  if (loading) return <div className="p-4">読み込み中...</div>;

  return (
    <TagListViewByDate
      date={date}
      tagList={tagList}
      memberList={[]} // memberList は空の配列を渡すか、propsから削除する
      onTagClick={handleTagClick}
      onEditClick={handleEditClick}
      onAddTagClick={handleAddTagClick}
      onCloseClick={handleCloseClick}
      message={error}
    />
  );
};

export default CommunityCalendarTagViewPage;

// M20 タグ編集画面 担当者: 浅野勇翔

import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Cookies from 'js-cookie';
import axios from "axios";

import TagPost from "../components/TagPost";

/**
 * TagEditPage コンポーネント
 * - 指定されたコミュニティIDと日付に対して、テンプレートタグを表示・選択
 * - 選択されたタグの該当日との紐づけを解除するAPIを呼び出す
 */
const TagEditPage = () => {
  // パラメータ取得
  const { communityId, date } = useParams();

  // ステート管理
  const [tagList, setTagList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const userId = Cookies.get('userId');
  const navigate = useNavigate();

  // タグ一覧取得
  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/calendar/${date}/tags`)
      .then((res) => {
        setTagList(res.data.tags || []);
      })
      .catch((err) => {
        console.error(err);
        setError("タグ一覧の取得に失敗しました");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [communityId]);

  // タグ追加API呼び出し
  const handleSubmit = (selectedId) => {
    if (!selectedId) return;

    axios
      .delete(`${process.env.REACT_APP_API_SERVER_URL}/api/calendar/${date}/tags`, {
        tag_id: selectedId,
        user_id: userId
      })
      .then(() => {
        navigate(`/community/${communityId}/calendar/${date}/tags/post/complate`);
      })
      .catch((err) => {
        console.error(err);
        alert("タグの削除に失敗しました");
      });
  };

  const handleClose = () => {
    navigate(`/community/${communityId}/calendar/${date}/tags/view`);
  }

  if (loading) return <div className="p-4">読み込み中...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <TagPost
      tagList={tagList}
      date={date}
      onSubmit={handleSubmit}
      onClickClose={handleClose}
    />
  );
};

export default TagEditPage;

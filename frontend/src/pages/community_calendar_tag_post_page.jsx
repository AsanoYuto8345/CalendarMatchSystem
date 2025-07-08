// M18 新規タグ入力画面（ロジック処理部） 担当者: 浅野勇翔

import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import Cookies from 'js-cookie';
import axios from "axios";

import TagPost from "../components/TagPost";

/**
 * TagPostPage コンポーネント
 * - 指定されたコミュニティIDと日付に対して、テンプレートタグを表示・選択
 * - 選択されたタグを該当日に紐づけるAPIを呼び出す
 */
const TagPostPage = () => {
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
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/template_tags?community_id=${communityId}`)
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
  const handleSubmit = (selectedTag) => {
    if (!selectedTag) return;

    axios
      .post(`${process.env.REACT_APP_API_SERVER_URL}/api/${communityId}/calendar/tag/add`, {
        tag_name: selectedTag.tag,
        tag_color: selectedTag.color_code,
        submitter_id: userId,
        date: date
      })
      .then((res) => {
        if(res.data.message === "指定された日付、登録者のタグは既に登録されています"){
          alert("指定されたタグは既に追加済みです");
        }else{
          navigate(`/community/${communityId}/calendar/${date}/tags/post/complate`);
        }
      })
      .catch((err) => {
        console.error(err);
        alert("タグの追加に失敗しました");
      });
  };

  const handleClose = () => {
    navigate(`/community/${communityId}/calendar/tags/${date}`);
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

export default TagPostPage;

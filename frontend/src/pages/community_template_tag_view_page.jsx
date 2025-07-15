// M17 テンプレートタグ一覧画面// 担当者: 浅野勇翔
// - コミュニティ ID に紐づくテンプレートタグ情報を API から取得し表示する
// - 表示には TemplateTagList コンポーネントを使用する

import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";

import TemplateTagView from "../components/TemplateTagView";

const TemplateTagViewPage = () => {
  // URL パラメータから communityId を取得
  const { communityId } = useParams();
  const navigate = useNavigate();
  // テンプレートタグ一覧を保持する state
  const [templateTags, setTemplateTags] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleteCount, setDeleteCount] = useState(0);
  const [error, setError] = useState("");

  const onClickEdit = (tagId) => {
    navigate(`/community/${communityId}/calendar/template_tag/${tagId}/edit`);
  }

  const onClickCreate = () => {
    navigate(`/community/${communityId}/calendar/template_tag/create`);
  }

  const onClickDelete = (tagId) => {
    setLoading(true);
    axios
      .delete(`${process.env.REACT_APP_API_SERVER_URL}/api/community/template_tags`,
        {
          data: { 
            "template_tag_id": tagId,
            "community_id": communityId
           }
        }
      )
      .then((res) => {
        setDeleteCount(deleteCount + 1);
      })
      .catch((err) => {
        console.error(err);
        setError("テンプレートタグの削除に失敗しました。");
      })
      .finally(() => {
        setLoading(false);
      });
  }


  // 初回レンダリング時に API からテンプレートタグを取得
  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/template_tags?community_id=${communityId}`)
      .then((res) => {
        setTemplateTags(res.data.tags || []);
      })
      .catch((err) => {
        console.error(err);
        setError("テンプレートタグの取得に失敗しました。");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [communityId, deleteCount]);

  // ローディング中
  if (loading) return <div className="p-4">読み込み中...</div>;

  // エラー発生時
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  console.log(deleteCount);

  return <TemplateTagView tags={templateTags} onClickEdit={onClickEdit} onClickCreate={onClickCreate} onClickDelete={onClickDelete} />;
};

export default TemplateTagViewPage;
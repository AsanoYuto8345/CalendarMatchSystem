// M16 テンプレートタグ編集画面(新規登録ver) 担当者: 浅野勇翔

import axios from "axios";
import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

import TemplateTagEdit from "../components/TemplateTagEdit";

/**
 * テンプレートタグ編集ページ(新規登録時)
 * - URL パラメータ communityId,を受け取って API から既存のタグ情報を取得
 *
 * 
 * 作成者: 浅野勇翔
 */
const TemplateTagCreatePage = () => {
  const { communityId } = useParams();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  
  const onSubmit = (tagName, colorCode) => {
    /**
   * 完了ボタン押下時の処理
   * - 入力されたタグ名とカラーコードを編集するようにAPIリクエストを行う
   */
    setLoading(true);
    axios
      .post(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/template_tags}`,
        {
          tag_name: tagName,
          color_code: colorCode
        }
      )
      .then((res) => {
        navigate(`community/${communityId}/calendar/template_tag/view`);
      })
      .catch((err) => {
        console.error(err);
        setError("タグ情報の追加に失敗しました");
      })
      .finally(() => {
        setLoading(false);
      });
  }

  if (loading) return <div className="p-4">読み込み中...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return <TemplateTagEdit tagName={""} colorCode={""} onSubmit={onSubmit}/>;
};

export default TemplateTagCreatePage;

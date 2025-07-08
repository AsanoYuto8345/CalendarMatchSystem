// M16 テンプレートタグ編集画面 担当者: 浅野勇翔

import axios from "axios";
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

import TemplateTagEdit from "../components/TemplateTagEdit";

/**
 * テンプレートタグ編集ページ
 * - URL パラメータ communityId, tagId を受け取って API から既存のタグ情報を取得
 * - 取得した情報を <TemplateTagEdit> に渡して編集画面を構築
 * 
 * 作成者: 浅野勇翔
 */
const TemplateTagEditPage = () => {
  const { communityId, tagId } = useParams();
  const [tagName, setTagName] = useState("");
  const [colorCode, setColorCode] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  
  const onSubmit = (tagName, colorCode) => {
    /**
   * 完了ボタン押下時の処理
   * - 入力されたタグ名とカラーコードを編集するようにAPIリクエストを行う
   */
    setLoading(true);
    axios
      .put(`${process.env.REACT_APP_API_SERVER_URL}/api/community/template_tags`,
        {
          tag: tagName,
          template_tag_id: tagId,  
          colorCode: colorCode,
          community_id: communityId
        }
      )
      .then((res) => {
        navigate(`/community/${communityId}/template_tag/view`);
      })
      .catch((err) => {
        console.error(err);
        setError("タグ情報の更新に失敗しました");
      })
      .finally(() => {
        setLoading(false);
      });
  }

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/template_tag_by_id?tag_id=${tagId}`)
      .then((res) => {
        const template_tag = res.data.template_tag;
        setTagName(template_tag.tag || "");
        setColorCode(template_tag.color_code || "");
      })
      .catch((err) => {
        console.error(err);
        setError("タグ情報の取得に失敗しました");
      })
      .finally(() => {
        setLoading(false);
      });
  }, [communityId, tagId]);

  if (loading) return <div className="p-4">読み込み中...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return <TemplateTagEdit tagName={tagName} colorCode={colorCode} onSubmit={onSubmit}/>;
};

export default TemplateTagEditPage;

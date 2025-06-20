// M16 テンプレートタグ編集画面 担当者: 浅野勇翔

import axios from "axios";
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

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

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/community/${communityId}/tags/${tagId}`)
      .then((res) => {
        setTagName(res.data.tag_name || "");
        setColorCode(res.data.color_code || "");
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

  return <TemplateTagEdit tagName={tagName} colorCode={colorCode} />;
};

export default TemplateTagEditPage;

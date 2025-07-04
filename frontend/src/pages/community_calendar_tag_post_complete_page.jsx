// M19 追加完了M 担当者: 浅野勇翔

import { useParams, useNavigate } from "react-router-dom";
import TagPostComplete from "../components/TagPostComplateMessage";

/**
 * TagPostCompleteMessagePage コンポーネント
 * 追加完了Mを表示するページ
 */

const TagPostCompleteMesaagePage = () => {
  const { communityId, date } = useParams();
  const navigate = useNavigate();

  const handleClose = () => {
    navigate(`/community/${communityId}/calendar/${date}/tags/view`);
  }

  return (
    <TagPostComplete onClose={handleClose} message={"追加"}/>
  );
}

export default TagPostCompleteMesaagePage;
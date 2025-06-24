// M19 追加完了M 担当者: 浅野勇翔

import { useParams, useNavigate } from "react-router-dom";
import TagPostComplete from "../components/TagPostComplateMessage";

/**
 * TagEditCompleteMessagePage コンポーネント
 * 編集完了Mを表示するページ
 */

const TagEditCompleteMesaagePage = () => {
  const { communityId } = useParams();
  const navigate = useNavigate();

  const handleClose = () => {
    navigate(`/community/${communityId}/calendar/:date/tags/view`);
  }

  return (
    <TagPostComplete onClose={handleClose} message={"編集"}/>
  );
}

export default TagEditCompleteMesaagePage;
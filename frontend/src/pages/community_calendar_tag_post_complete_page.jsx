import { useParams, useNavigate } from "react-router-dom";
import TagPostComplete from "../components/TagPostComplateMessage";

const TagPostCompleteMesaagePage = () => {
  const { communityId } = useParams();
  const navigate = useNavigate();

  const handleClose = () => {
    navigate(`/community/${communityId}/calendar/:date/tags/view`);
  }

  return (
    <TagPostComplete onClose={handleClose}/>
  );
}

export default TagPostCompleteMesaagePage;
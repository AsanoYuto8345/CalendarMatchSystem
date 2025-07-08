// M9 ユーザ情報編集画面 担当: 角田一颯

import axios from "axios";
import Cookies from "js-cookie";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import UserInfoEdit from "../components/UserInfoEdit";

/**
 * ユーザ情報編集ページ
 * - Cookie からユーザIDを取得
 * - プロフィール情報を取得・編集する
 */
const UserInfoEditPage = () => {
  const userId = Cookies.get("userId");
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [iconUrl, setIconUrl] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  // 初期ユーザ情報の取得
  useEffect(() => {
    // if (!userId) {
    //   setError("ユーザIDが見つかりません (E1)");
    //   setLoading(false);
    //   return;
    // }

    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/user/${userId}`)
      .then((res) => {
        const { name, email, icon_url } = res.data;
        setName(name);
        setEmail(email);
        setIconUrl(icon_url);
      })
      .catch((err) => {
        // console.error(err);
        // setError("ユーザ情報の取得に失敗しました (E2)");
      })
      .finally(() => setLoading(false));
  }, [userId]);

  // 送信ハンドラ
  const handleSubmit = async ({ name, pw, iconFile }) => {
    try {
      const formData = new FormData();
      formData.append("name", name);
      if (pw) formData.append("pw", pw);
      if (iconFile) formData.append("icon", iconFile);

      await axios.put(`${process.env.REACT_APP_API_SERVER_URL}/api/user/${userId}`, formData);

      // 編集完了後に遷移
      navigate("/user/profile");
    } catch (err) {
      console.error(err);
      setError("ユーザ情報の更新に失敗しました");
    }
  };

  if (loading) return <div className="p-4">読み込み中...</div>;
  if (error) return <div className="p-4 text-red-500">{error}</div>;

  return (
    <UserInfoEdit
      name={name}
      iconUrl={iconUrl}
      onSubmit={handleSubmit}
    />
  );
};

export default UserInfoEditPage;

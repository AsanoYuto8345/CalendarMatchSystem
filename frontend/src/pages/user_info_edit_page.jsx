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
  const userId = Cookies.get("userId"); // ユーザーIDはCookieから取得
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [iconUrl, setIconUrl] = useState(""); // UIで表示するアイコンURL
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  // 初期ユーザ情報の取得
  useEffect(() => {
    if (!userId) {
      setError("ユーザIDが見つかりません。ログインしてください。");
      setLoading(false);
      // navigate("/login"); // 必要ならログインページへ
      return;
    }

    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/user/get/${userId}`)
      .then((res) => {
        const { user_data } = res.data;
        setName(user_data.name);
        setEmail(user_data.email);
        setIconUrl(user_data.icon_name); // 表示用に設定
      })
      .catch((err) => {
        console.error("ユーザ情報の取得に失敗しました:", err);
        setError("ユーザ情報の取得に失敗しました。");
      })
      .finally(() => setLoading(false));
  }, [userId, navigate]);

  // 送信ハンドラ
  const handleSubmit = async ({ name, pw, iconFile }) => {
    try {
      const formData = new FormData();
      formData.append("user_id", userId);
      formData.append("name", name);
      if (pw) {
        formData.append("password", pw);
      }
      if (iconFile) {
        formData.append("icon_file", iconFile);
      }

      await axios.put(`${process.env.REACT_APP_API_SERVER_URL}/api/user/edit`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // 完了ページへ遷移
      navigate(`/user/${userId}/edit/complete`);
    } catch (err) {
      console.error("ユーザ情報の更新に失敗しました:", err.response ? err.response.data : err);
      setError(err.response?.data?.error || "ユーザ情報の更新に失敗しました");
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
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
      // 必要であればログインページへリダイレクト
      // navigate("/login");
      return;
    }

    axios
      .get(`${process.env.REACT_APP_API_SERVER_URL}/api/user/get/${userId}`) // GETエンドポイントを修正
      .then((res) => {
        const { user_data } = res.data; // レスポンスの構造が { user_data: {...} } に変更されている
        setName(user_data.name);
        setEmail(user_data.email);
        setIconUrl(user_data.icon_name); // icon_name を iconUrl としてセット
      })
      .catch((err) => {
        console.error("ユーザ情報の取得に失敗しました:", err);
        setError("ユーザ情報の取得に失敗しました。");
      })
      .finally(() => setLoading(false));
  }, [userId, navigate]); // navigate を依存配列に追加

  // 送信ハンドラ
  const handleSubmit = async ({ name, pw, iconFile }) => {
    try {
      const formData = new FormData();
      formData.append("user_id", userId); // user_id を FormData に追加
      formData.append("name", name);
      // パスワードが入力されている場合のみ追加
      if (pw) {
        formData.append("password", pw); // キーを "password" に修正
      }
      // アイコンファイルが選択されている場合のみ追加
      if (iconFile) {
        formData.append("icon_file", iconFile); // キーを "icon_file" に修正
      } else if (iconFile === null && iconUrl !== "") {
        // アイコンをクリアしたい場合など、iconFileがnullで元々アイコンがあった場合
        // 例えば、UIに「アイコンを削除」ボタンを設け、そのボタンが押されたときに
        // `setNewIconFile(false)` のような状態をセットして、`data_edit`に伝える。
        // 現状のUIでは「アイコン画像を選択」しかないので、このケースは発生しないが、
        // 将来的な拡張のためにコメントとして残しておく。
        // formData.append("icon_file", ""); // または特別なフラグ
      }


      // PUTリクエストのURLとデータの形式を修正
      await axios.put(`${process.env.REACT_APP_API_SERVER_URL}/api/user/edit`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // ファイルを送信するため必要
        },
      });

      // 編集完了後に遷移
      navigate("/user/profile"); // 適切な遷移先に変更してください
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

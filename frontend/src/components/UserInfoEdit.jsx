// W19 ユーザ情報編集画面に対応するReactコンポーネント 担当: 角田一颯

import { useState, useRef } from "react";

/**
 * ユーザ編集用フォーム（カメラアイコンで画像アップロード）
 */
const UserInfoEdit = ({ name = "", iconUrl = "", onSubmit }) => {
  const [newName, setNewName] = useState(name);
  const [newPw, setNewPw] = useState("");
  const [newIconFile, setNewIconFile] = useState(null);
  const [previewIcon, setPreviewIcon] = useState(iconUrl);
  const [error, setError] = useState(""); // ← エラーメッセージ用ステート追加

  // input fileの参照を保持
  const fileInputRef = useRef(null);

  // カメラボタン押したらファイル選択ダイアログを開く
  const handleCameraClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  // ファイル選択時
  const handleIconChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setNewIconFile(file);
      const reader = new FileReader();
      reader.onload = () => setPreviewIcon(reader.result);
      reader.readAsDataURL(file);
    }
  };

  // 送信処理（バリデーションあり）
  const handleSubmit = () => {
    // 表示名のバリデーション
    if (newName.length > 20) {
      setError("表示名は20文字以内で入力してください。");
      return;
    }

    // パスワードのバリデーション（空でない場合のみチェック）
    if (newPw) {
      if (newPw.length > 20) {
        setError("パスワードは20文字以内で入力してください。");
        return;
      }
      if (!/^[A-Za-z0-9]+$/.test(newPw)) {
        setError("パスワードは半角英数字のみ使用できます。");
        return;
      }
    }

    // バリデーション通過 → エラー解除＆送信
    setError("");
    onSubmit({
      name: newName,
      pw: newPw || undefined,
      iconFile: newIconFile,
    });
  };

  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold text-center mb-6">プロフィール編集</h2>

      <div className="mb-4">
        <label className="block text-gray-700 mb-2">表示名</label>
        <input
          className="w-full px-3 py-2 border rounded"
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          maxLength={20} // ← 入力制限（補助的）
        />
      </div>

      <div className="mb-4">
        <label className="block text-gray-700 mb-2">パスワード（変更する場合のみ）</label>
        <input
          className="w-full px-3 py-2 border rounded"
          type="password"
          value={newPw}
          onChange={(e) => setNewPw(e.target.value)}
          maxLength={20} // ← 入力制限（補助的）
          pattern="[A-Za-z0-9]*"
        />
      </div>

      <div className="mb-6">
        <label className="block text-gray-700 mb-2">アイコン画像</label>

        {/* プレビュー画像 */}
        {previewIcon ? (
          <img
            src={previewIcon}
            alt="画像"
            className="w-24 h-24 mb-2 rounded-full object-cover"
          />
        ) : (
          <div className="w-24 h-24 mb-2 bg-gray-200 rounded-full flex items-center justify-center text-gray-500">
            No Image
          </div>
        )}

        {/* ファイル入力は非表示 */}
        <input
          type="file"
          accept="image/*"
          onChange={handleIconChange}
          ref={fileInputRef}
          className="hidden"
        />

        {/* カメラマークのボタン */}
        <button
          type="button"
          onClick={handleCameraClick}
          className="inline-flex items-center px-3 py-1 border rounded text-gray-600 hover:text-gray-900 hover:border-gray-900"
          aria-label="アイコン画像を選択"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6 mr-2"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 7h4l3-3h4l3 3h4v11H3V7z"
            />
            <circle cx="12" cy="13" r="3" stroke="currentColor" strokeWidth={2} />
          </svg>
          アイコン画像を選択
        </button>
      </div>

      {/* エラーメッセージ表示 */}
      {error && (
        <div className="mb-4 text-red-500 text-sm text-center">
          {error}
        </div>
      )}

      <button
        className="w-full py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        onClick={handleSubmit}
      >
        保存
      </button>
    </div>
  );
};

export default UserInfoEdit;

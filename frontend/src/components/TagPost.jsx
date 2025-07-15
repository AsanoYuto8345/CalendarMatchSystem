// W11 新規タグ入力画面（UIコンポーネント）担当者: 浅野勇翔

import { useState } from "react";

/**
 * TemplateTagSelect コンポーネント
 * - テンプレートタグの一覧から選択できるラジオボタン式UIを表示
 * - 完了ボタンで選択結果を親に通知する
 *
 * Props:
 * - tagList: { id: string, name: string, color: string }[] - タグ一覧
 * - onSubmit: (selectedTagId: string) => void - 完了時に呼ばれる関数
 * - onClickClose: () => void - ×ボタンを押したときに呼ばれる関数
 */
const TagPost = ({ tagList = [], date ,onSubmit, onClickClose, title = "テンプレートタグ一覧" }) => {
  const [selectedTag, setSelectedTag] = useState({});

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-gradient-to-b from-white to-gray-100 rounded shadow">
      {/* ヘッダー部 */}
      <div className="flex justify-between items-center mb-4">
        <div className="text-sm text-gray-500">{date}</div>
        <button className="text-lg font-bold" onClick={onClickClose}>×</button>
      </div>

      {/* タイトル */}
      <h2 className="text-center text-lg font-semibold mb-4">{title}</h2>

      {/* ラジオボタン付きタグリスト */}
      <div className="space-y-3 mb-6">
        {tagList.map((tag) => (
          <label
            key={tag.id}
            className="flex items-center gap-4 cursor-pointer bg-gray-100 p-3 rounded-md"
          >
            <input
              type="radio"
              name="templateTag"
              value={tag.id}
              checked={selectedTag?.id === tag.id}
              onChange={() => setSelectedTag(tag)}
              className="w-5 h-5"
            />
            <div
              className="flex-1 text-lg px-3 py-2 rounded font-semibold truncate"
              style={{
                backgroundColor: `#${tag.color_code}`,
                color: '#fff',
                // 白文字＋黒縁取りのテキストシャドウ
                textShadow: '-1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000'
              }}
              title={tag.tag}
            >
              {tag.tag}
            </div>
          </label>
        ))}
      </div>

      {/* 完了ボタン */}
      <div className="text-center">
        <button
          onClick={() => onSubmit(selectedTag)}
          className="bg-white border px-6 py-2 rounded shadow hover:bg-gray-100"
        >
          完了
        </button>
      </div>
    </div>
  );
};

export default TagPost;

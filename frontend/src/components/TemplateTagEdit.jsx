// M9 テンプレートタグ編集画面表示コンポーネント // 担当者: 浅野勇翔

import { useState } from "react";

/**
 * TemplateTagEdit コンポーネント
 * 
 * Props:
 * - tagName: string（初期値。日本語・英数字最大20文字）
 * - colorCode: string（初期値。英数字6文字）
 */
const TemplateTagEdit = ({ tagName = "", colorCode = "000000" }) => {
  const [tag, setTag] = useState(tagName);
  const [color, setColor] = useState(colorCode);

  const onSubmit = () => {
    // バリデーションと送信処理は呼び出し元が担当
    alert(`タグ名: ${tag}, カラーコード: ${color}`);
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-gradient-to-b from-white to-gray-100 rounded shadow">
      <h2 className="text-center text-lg font-semibold mb-6">テンプレートタグ編集</h2>

      <div className="mb-4 flex items-center">
        <label className="w-24 text-right mr-4">タグ名</label>
        <input
          type="text"
          className="border px-2 py-1 w-full"
          value={tag}
          onChange={(e) => setTag(e.target.value)}
        />
        <span className="ml-2 text-sm text-gray-500 whitespace-nowrap">日本語,英数字(20字以内)</span>
      </div>

      <div className="mb-6 flex items-center">
        <label className="w-24 text-right mr-4">カラーコード</label>
        <input
          type="text"
          className="border px-2 py-1 w-full"
          value={color}
          onChange={(e) => setColor(e.target.value)}
        />
        <span className="ml-2 text-sm text-gray-500 whitespace-nowrap">英数字(6字)</span>
      </div>

      <div className="text-center">
        <button
          className="bg-white border px-4 py-1 rounded shadow hover:bg-gray-100"
          onClick={onSubmit}
        >
          完了
        </button>
      </div>
    </div>
  );
};

export default TemplateTagEdit;

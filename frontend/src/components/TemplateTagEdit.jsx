// M16 テンプレートタグ編集画面（UIコンポーネント）
// 担当者: 浅野勇翔

import { useState } from "react";

/**
 * TemplateTagEdit コンポーネント
 * - テンプレートタグの編集フォーム
 * - props で初期値（tagName, colorCode）を受け取り、入力可能なフォームを表示
 * - 入力に応じてリアルタイムに色プレビューを表示
 *
 * Props:
 *  - tagName (string): 初期タグ名（省略時は空文字）
 *  - colorCode (string): 初期カラーコード（6桁の16進数, 省略時は "000000"）
 */
const TemplateTagEdit = ({ tagName = "", colorCode = "000000" }) => {
  const [tag, setTag] = useState(tagName);
  const [color, setColor] = useState(colorCode);

  /**
   * 完了ボタン押下時の処理
   * - 入力されたタグ名とカラーコードをアラート表示（将来的にはAPI送信）
   */
  const onSubmit = () => {
    alert(`タグ名: ${tag}, カラーコード: ${color}`);
  };

  // 表示用のカラーコード。#がなければ補う。
  const displayColor = color.startsWith("#") ? color : `#${color}`;

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-gradient-to-b from-white to-gray-100 rounded shadow">
      <h2 className="text-center text-lg font-semibold mb-6">テンプレートタグ編集</h2>

      {/* タグ名入力フォーム */}
      <div className="mb-4">
        <label className="block text-sm font-medium mb-1">タグ名</label>
        <input
          type="text"
          className="border px-3 py-2 w-full rounded"
          value={tag}
          onChange={(e) => setTag(e.target.value)}
          placeholder="例: 会議, 作業時間"
        />
        <p className="text-sm text-gray-500 mt-1">日本語,英数字（20字以内）</p>
      </div>

      {/* カラーコード入力フォーム + 色プレビュー */}
      <div className="mb-6">
        <label className="block text-sm font-medium mb-1">カラーコード</label>
        <div className="flex items-center gap-4">
          <input
            type="text"
            className="border px-3 py-2 w-full rounded"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            placeholder="例: FF0000"
          />
          {/* 色のサンプルボックス */}
          <div
            className="w-8 h-8 border rounded"
            style={{ backgroundColor: displayColor }}
            title={displayColor}
          />
        </div>
        <p className="text-sm text-gray-500 mt-1">英数字（6桁の16進数）</p>
      </div>

      {/* 完了ボタン */}
      <div className="text-center">
        <button
          className="bg-white border px-6 py-2 rounded shadow hover:bg-gray-100"
          onClick={onSubmit}
        >
          完了
        </button>
      </div>
    </div>
  );
};

export default TemplateTagEdit;

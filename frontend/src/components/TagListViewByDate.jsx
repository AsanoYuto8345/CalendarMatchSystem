import React from 'react';
import { Link } from 'react-router-dom';

/**
 * W15 日付ごとのタグ一覧画面に対応するReactコンポーネント
 * @param {object} props - コンポーネントのプロパティ
 * @param {string} props.date - 表示対象の日付 (例: "XX/XX/20XX")
 * @param {Array<object>} props.tagList - 該当日付に投稿されたタグのリスト
 * @param {Array<object>} props.memberList - 該当日付にタグを投稿したメンバーのリスト
 * @param {Function} props.onTagClick - タグクリック時のハンドラ
 * @param {Function} props.onEditClick - 編集ボタンクリック時のハンドラ
 * @param {Function} props.onAddTagClick - 新規タグ追加ボタンクリック時のハンドラ
 * @param {Function} props.onCloseClick - 閉じるボタンクリック時のハンドラ
 * @param {string} props.message - 表示メッセージ
 *
 * 作成者: (TBD)
 */
const TagListViewByDate = ({ date, tagList, memberList, onTagClick, onEditClick, onAddTagClick, onCloseClick, message }) => {
  console.log(tagList);
  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-white shadow-lg rounded-lg">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">{date}</h2>
        <button onClick={onCloseClick} className="text-gray-500 hover:text-gray-700 text-xl font-bold">
          X
        </button>
      </div>

      {message && <p className="text-center text-red-500 mb-4">{message}</p>}

      <h3 className="text-xl font-semibold mb-3">タグ一覧</h3>
      {tagList.length > 0 ? (
        tagList.map((tag, index) => (
          <div key={index} className="flex justify-between items-center bg-gray-100 p-3 rounded-md mb-2">
            {/* タグの名前と色を表示する部分 */}
            <div
              className="flex-1 text-lg px-3 py-1 rounded font-semibold text-white truncate"
              style={{
                backgroundColor: `#${tag.color}`, // tag.color を背景色に適用
                textShadow: "0 0 2px rgba(0,0,0,0.7)" // テキストの視認性を高めるためのシャドウ
              }}
            >
              {tag.name}
            </div>
            <button onClick={() => onTagClick(tag.id)} className="ml-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
              チャットへ
            </button>
          </div>
        ))
      ) : (
        <p className="text-gray-600 mb-4">この日付にはタグがありません。</p>
      )}

      <div className="flex justify-center space-x-4 mt-6">
        <button onClick={onEditClick} className="px-6 py-2 bg-green-500 text-white rounded hover:bg-green-600">
          編集
        </button>
        <button onClick={onAddTagClick} className="px-6 py-2 bg-purple-500 text-white rounded hover:bg-purple-600">
          新規タグ追加
        </button>
      </div>
    </div>
  );
};

export default TagListViewByDate;

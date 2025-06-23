// W12 新規タグ追加完了画面（UIコンポーネント) 担当者: 浅野勇翔

/**
 * TagPostComplete コンポーネント
 * - タグの追加完了を通知する画面
 * - 閉じる（×）ボタンで onClose を発火
 *
 * Props:
 * - onClose: 閉じる処理を行う関数
 */
const TagPostCompleteMessage = ({ onClose }) => {
  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white border rounded shadow relative">
      {/* 閉じるボタン（右上） */}
      <button
        className="absolute top-2 right-2 text-gray-500 hover:text-gray-800 text-xl"
        onClick={onClose}
        aria-label="閉じる"
      >
        ×
      </button>

      {/* 完了メッセージ */}
      <div className="text-center text-lg font-medium text-gray-800 mt-6">
        追加完了
      </div>
    </div>
  );
};

export default TagPostCompleteMessage;

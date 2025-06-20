// W7 コミュニティ脱退画面に対応するReactコンポーネント 担当者: 浅野勇翔 

const CommunityLeave = ({ communityName = "未設定", onAcceptClick, onRejectClick, msg }) => {
  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-white shadow-lg rounded-lg">
      {/* タイトル */}
      <h2 className="text-2xl font-bold text-center mb-4">
        コミュニティ脱退
      </h2>

      {/* 対象コミュニティ名 */}
      <p className="text-center text-lg mb-6">
        <span className="font-semibold">{communityName}</span> から脱退しますか？
      </p>

      {/* ボタン */}
      <div className="flex justify-center space-x-4 mb-6">
        <button
          className="px-6 py-2 bg-red-500 hover:bg-red-600 text-white rounded"
          onClick={onAcceptClick}
        >
          はい
        </button>
        <button
          className="px-6 py-2 bg-gray-300 hover:bg-gray-400 text-gray-800 rounded"
          onClick={onRejectClick}
        >
          いいえ
        </button>
      </div>

      {/* 処理メッセージ */}
      <div>{msg}</div>
    </div>
  );
};

export default CommunityLeave;
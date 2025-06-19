/**
 * W17 ログアウトUIコンポーネント
 * - ログアウト確認ダイアログ
 * 作成者: 石田めぐみ
 */

const LogoutUI = ({ onAcceptClick, onRejectClick }) => {
  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-bold text-center mb-4">ログアウト</h2>
      <p className="text-center text-lg mb-6">
        ログアウトしますか？
      </p>

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
    </div>
  );
};

export default LogoutUI;
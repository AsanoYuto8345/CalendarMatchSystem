// W10 テンプレートタグ一覧画面に対応するReactコンポーネント // 担当者: 浅野勇翔

/**
 * TemplateTagPage コンポーネント
 * - テンプレートタグを一覧表示し、編集と新規作成ボタンを表示する
 * - 編集・新規作成の処理は props から関数として受け取る
 *
 * Props:
 * - tags: タグオブジェクトの配列（{ id, name }）
 * - onClickEdit: 編集ボタン押下時の関数（引数に tag.id が渡される）
 * - onClickCreate: 新規作成ボタン押下時の関数
 */
const TemplateTagView = ({ tags = [], onClickEdit, onClickCreate }) => {
  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-gradient-to-b from-white to-gray-100 rounded shadow">
      {/* タイトル */}
      <h2 className="text-center text-lg font-semibold mb-6">テンプレートタグ一覧</h2>

      {/* タグの入力欄と編集ボタン */}
      <div className="space-y-4 mb-6">
        {tags.map((tag) => (
          <div key={tag.id} className="flex items-center gap-4">
            <input
              type="text"
              value={tag.name}
              readOnly
              className="border px-3 py-2 w-full rounded bg-gray-100 text-gray-700"
            />
            <button
              onClick={() => onClickEdit(tag.id)}
              className="px-4 py-1 bg-white border rounded hover:bg-gray-100"
            >
              編集
            </button>
          </div>
        ))}
      </div>

      {/* 新規作成ボタン */}
      <div className="text-center">
        <button
          onClick={onClickCreate}
          className="px-6 py-2 bg-white border rounded shadow hover:bg-gray-100"
        >
          新規作成
        </button>
      </div>
    </div>
  );
};

export default TemplateTagView;

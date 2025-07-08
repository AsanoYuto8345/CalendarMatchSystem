// W10 テンプレートタグ一覧画面に対応するReactコンポーネント
// 担当者: 浅野勇翔

/**
 * TemplateTagView コンポーネント
 * - テンプレートタグを一覧表示し、編集と新規作成ボタンを表示する
 * - inputの背景色をタグのカラーコードに応じて変化させる
 *
 * Props:
 * - tags: タグオブジェクトの配列（{ name, color, id }）
 * - onClickEdit: 編集ボタン押下時の関数（引数に tag.id が渡される）
 * - onClickCreate: 新規作成ボタン押下時の関数
 */
const TemplateTagView = ({ tags = [], onClickEdit, onClickCreate, onClickDelete }) => {
  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-gradient-to-b from-white to-gray-100 rounded shadow">
      {/* タイトル */}
      <h2 className="text-center text-lg font-semibold mb-6">
        テンプレートタグ一覧
      </h2>

      {/* タグリスト */}
      <div className="space-y-4 mb-6">
        {tags.map((tag) => (
          <div key={tag.id} className="flex items-center gap-4">
            {/* タグ名（背景色にカラーを適用） */}
            <input
              type="text"
              value={tag.tag}
              readOnly
              className="border px-3 py-2 w-full rounded font-semibold text-white"
              style={{
                backgroundColor: `#${tag.color_code}`,
                textShadow: "0 0 2px black", // 黒いアウトライン風のシャドウを追加
              }}
              title={`カラーコード: #${tag.color_code}`}
            />

            {/* 編集ボタン */}
            <button
              onClick={() => onClickEdit(tag.id)}
              className="px-4 py-1 bg-white border rounded hover:bg-gray-100"
            >
              編集
            </button>

            {/* 削除ボタン */}
            <button
              onClick={() => onClickDelete(tag.id)}
              className="px-4 py-1 bg-white border rounded hover:bg-gray-100"
            >
              削除
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

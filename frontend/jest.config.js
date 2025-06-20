// CalendarMatchSystem/frontend/jest.config.js
module.exports = {
  // テストの実行環境をブラウザライクなDOM環境に設定
  // 変更前: testEnvironment: 'jsdom',
  // 変更後:
  testEnvironment: 'jest-environment-jsdom', // ここをこのように変更
  // ★この行を新たに追加
  testEnvironmentOptions: {
    customExportConditions: ['node', 'node-addons'],
  },

  // 各テストファイル実行前にロードするセットアップファイル
  // setupTests.js が src/ ディレクトリ直下にあるので、そのパスを指定します。
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],

  // 特定のファイルをどのように変換するかを定義
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest', // .jsおよび.jsxファイルをbabel-jestで変換
  },

  // モジュールのエイリアスやモックの定義
  moduleNameMapper: {
    // CSSファイルをインポートした際に、空のオブジェクトとして扱う（テスト中にCSSを評価しないため）
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    // logo.svg のような画像ファイルをインポートした際に、モックとして扱う
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$': '<rootDir>/__mocks__/fileMock.js',
  },

  // テストとして認識しないパスを指定（コーディング規約を考慮）
  testPathIgnorePatterns: [
    '/node_modules/',
    '/public/', // 公開用静的ファイル（もしあれば）
    '/data/'    // バックエンドのSQLiteデータファイル（ frontend/ 直下には通常ないが、念のため）
  ],

  // テストカバレッジ（テストがコードのどれくらいを網羅しているか）を収集
  collectCoverage: true,
  // カバレッジレポートの出力先ディレクトリ
  coverageDirectory: 'coverage',
  // カバレッジ収集の対象ファイル（srcディレクトリ下のjs/jsxファイル）
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    '!src/**/*.d.ts', // TypeScriptの型定義ファイルを除外
    '!src/index.js',  // アプリケーションのエントリーポイントは通常テストしない
    '!src/reportWebVitals.js', // create-react-appで生成されるファイル
    '!src/setupTests.js', // テスト設定ファイル自体はカバレッジ対象外
    '!src/logo.svg', // logo.svgもカバレッジ対象外
    // 必要に応じて、テスト対象外のファイルをここに追加
  ],
};
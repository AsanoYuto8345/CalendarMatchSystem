#単体テスト(フロントエンド)
```bash
npm install --save-dev @testing-library/jest-dom @testing-library/react @testing-library/user-event
```
```bash
npm install react-router-dom
```
これができたらセットアップ完了
componentsディレクトリに
(テストしたいファイル名).test.jsxを作成
イメージ
```
.
├── CommunityLeave.jsx
├── LoginUI.jsx
├── LogoutUI.jsx
├── SignupUI.jsx
└── SignupUI.test.jsx
```
SignupUI.test.jsxの中身はcomponentsとpagesの該当ファイル投げてAIに作らせればいい
できたら
```bash
npm test     
```
する。
FAILなら
出てきた結果をAIに投げて修正
PASSなら
完成
こんな感じになる
```
 PASS  src/components/SignupUI.test.jsx
```
もしかしたら出てくるこいつ、多分こっちは無視していい
```
 FAIL  src/App.test.js
```


# カレンダーアプリケーション (Calendar App)

このリポジトリは、**Flask + SQLite** をバックエンドに、**React (Create React App)** をフロントエンドに用いた簡易カレンダーアプリケーションです。  
**Docker** は使用せず、全てローカル環境で立ち上げ・開発を行う前提の構成になっています。

---

## 目次

1. プロジェクト概要  
2. 前提条件  
3. リポジトリのクローン  
4. ローカル環境でのセットアップ手順  
   1. バックエンド (Flask＋SQLite)  
   2. フロントエンド (React)  
   3. 動作確認  
5. モジュール (パッケージ) の追加方法  
   1. バックエンドに新しいパッケージを追加する  
   2. フロントエンドに新しいパッケージを追加する  
6. ファイル変更の反映方法  
7. よくあるトラブルシュート  
8. プロジェクト構成・ファイル説明  
9. Gitフック (`post-merge`) の利用  
10. ライセンス  

---

## プロジェクト概要

- **バックエンド**：Python + Flask + SQLite  
  - REST API を提供し、`/api/messages` でサンプルのメッセージ一覧を JSON で返します  
  - Flask-CORS を使ってフロントからのリクエストを許可  
  - SQLite データベースにメッセージを永続化  

- **フロントエンド**：React (Create React App)  
  - バックエンドから取得したメッセージを画面に一覧表示  
  - 開発用サーバーにホットリロード機能を備え、ファイルを保存すると自動でブラウザが更新  

- **ローカル起動のみ**  
  - 全ての開発・動作確認はローカル環境（Node.js＋npm、Python＋pip）で行います  
  - Docker やコンテナは使いません

---

## 前提条件

1. **Node.js (v16 以上) と npm**  
   - [Node.js 公式サイト](https://nodejs.org/) からインストール  
2. **Python 3.8 以上 と pip**  
   - [Python 公式サイト](https://www.python.org/) からインストール  
3. ブラウザ（Chrome, Firefox, Safari など）

---

## リポジトリのクローン

```bash
git clone https://github.com/AsanoYuto8345/CalendarMatchSystem.git
cd CalendarMatchSystem
```

---

## ローカル環境でのセットアップ手順

### バックエンド (Flask＋SQLite)

1. **バックエンドディレクトリへ移動**  
   ```bash
   cd backend
   ```

2. **依存パッケージをインストール**  
   ```bash
   pip install --upgrade pip
   pip install --no-cache-dir -r requirements.txt
   ```

3. **サーバーを起動（開発モード）**  

   - ターミナルで：
     ```bash
     python app.py
     ```
   - 成功すると：
     ```
     * Serving Flask app "app"
     * Debug mode: on
     * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
     ```

4. **動作確認**  
   ```bash
   # 別ターミナルまたはブラウザで
   curl http://localhost:5000/api/messages
   ```
   - またはブラウザで `http://localhost:5000/api/messages` にアクセスし、JSON レスポンスが取得できることを確認してください。

---

### フロントエンド (React)

1. **フロントエンドディレクトリへ移動**  
   ```bash
   cd ../frontend
   ```

2. **依存パッケージをインストール**  
   ```bash
   npm install
   ```

3. **開発サーバーを起動（ホットリロード有効）**  
   ```bash
   npm start
   ```
   - 以下のようなログが出て、React サーバーが立ち上がります：
     ```
     ℹ ｢wds｣: Project is running at http://0.0.0.0:3000/
     ℹ ｢wds｣: webpack output is served from /
     ℹ ｢wds｣: Content not from webpack is served from /app/public
     ℹ ｢wds｣: 404s will fallback to /index.html
     ```
   - ブラウザで `http://localhost:3000` にアクセスし、React アプリのトップページを表示してください。

4. **動作確認**  
   - ブラウザ開発者ツールの Console や Network タブを見て、`http://localhost:5000/api/messages` へのリクエストが成功し、  
     メッセージ一覧がフロントに表示されることを確認します。

---

## モジュール (パッケージ) の追加方法

### バックエンドに新しいパッケージを追加する

1. **`requirements.txt` に追記**  
   例として `python-dotenv` を追加する場合：
   ```
   Flask==2.2.5
   Flask-Cors==3.0.10
   Flask-SQLAlchemy==3.0.5
   gunicorn==20.1.0
   python-dotenv==1.0.0   # 追加
   ```

2. **ローカル環境でインストール → バージョン固定**  
   ```bash
   cd backend
   pip install python-dotenv
   pip freeze > requirements.txt
   ```
   - `pip freeze` を使うと今インストールされている全パッケージがバージョン付きで `requirements.txt` に書き出されます。

3. **動作確認**  
   ```bash
   python app.py
   ```
   - 新しく入れたパッケージが正しく読み込まれるかを確認します。

---

### フロントエンドに新しいパッケージを追加する

1. **パッケージをインストール**  
   例として `axios` を入れる場合：
   ```bash
   cd frontend
   npm install axios --save
   ```
   - `--save` を付けると `package.json` の `dependencies` に自動追記されます。

2. **コミット**  
   ```bash
   git add frontend/package.json frontend/package-lock.json
   git commit -m "feat: add axios for API calls"
   ```

3. **動作確認**  
   ```bash
   npm start
   ```
   - `axios` を使った API 呼び出しコードを書いて、正しく動作するかを確認します。

---

## ファイル変更の反映方法

### フロントエンド

1. **`npm start` 中にファイルを保存**  
2. ターミナルログに以下のような再ビルドメッセージが出れば OK：
   ```
   [HMR] rebuild started
   [HMR] rebuild finished in xxx ms
   ℹ ｢wds｣: Compiled successfully!
   ```
3. ブラウザが自動的に再読み込みされ、変更内容が反映されます。  
   - もし動作しない場合は、React-Scripts のバージョンが 5.x 以上か、`node_modules` が揮発していないかをチェックしてください。

### バックエンド

1. **`python app.py` 中に `.py` ファイルを保存**  
2. ターミナルログに以下のような再起動メッセージが出れば OK：
   ```
   * Detected change in 'app.py', reloading
   ```
3. 再び `http://localhost:5000/api/messages` にアクセスし、変更が反映されているかを確認します。  

---

## よくあるトラブルシュート

1. **フロントが起動しない (`react-scripts` 関連エラー)**  
   - `node_modules` フォルダを削除し、再度 `npm install` を実行する  
   - `npm cache clean --force` → `npm install` を試す  
   - `react-scripts` を最新版（5.x）にアップグレードし、`rm -rf node_modules package-lock.json` → `npm install`  

2. **バックエンドが起動しない (ImportError, ModuleNotFoundError)**  
   - 仮想環境を正しくアクティベートしているか確認  
   - `requirements.txt` に必要なパッケージが漏れていないか確認し、`pip install -r requirements.txt` を再実行する  

3. **CORS エラー (“No ‘Access-Control-Allow-Origin’ header” が出る)**  
   - `backend/app.py` 内で `Flask-CORS` がインポート・初期化されているか確認：
     ```python
     from flask_cors import CORS
     app = Flask(__name__)
     CORS(app)
     ```
   - これで `Access-Control-Allow-Origin: *` がレスポンスヘッダに付与されるはずです。  

4. **ファイル変更を保存しても再ビルドされない（ホットリロードが効かない）**  
   - フロントエンド側で `react-scripts` が v5.x 以上かを確認  
   - Windows / WSL2 環境ではファイルイベント通知が不安定なことがあるため、  
     ```bash
     CHOKIDAR_USEPOLLING=true CHOKIDAR_INTERVAL=100 npm start
     ```
     のように環境変数を付けて “ポーリング監視” モードに切り替えてみてください。  

5. **SQLite ファイル (`*.db`) が Git にコミットされてしまう**  
   - `.gitignore` に `*.db` が含まれているか確認し、含まれていなければ追加してください。  

---

## プロジェクト構成・ファイル説明

```
calendar-app/
├─ backend/                    # バックエンド (Flask + SQLite)
│   ├─ app.py                  # Flask アプリ本体
│   ├─ requirements.txt        # Python パッケージ一覧
│   ├─ messages.db             # SQLite データベースファイル（.gitignore で除外）
│   └─ __pycache__/            # Python コンパイル済みキャッシュ（.gitignore で除外）
│
├─ frontend/                   # フロントエンド (React)
│   ├─ public/                 # CRA の public フォルダ (index.html など)
│   ├─ src/                    # React コンポーネントやスタイルなど
│   │   └─ App.js              # メインコンポーネント
│   ├─ node_modules/           # npm 依存モジュール（.gitignore で除外）
│   ├─ package.json            # Node.js / React の依存定義およびスクリプト
│   ├─ package-lock.json       # バージョン固定ファイル
│   └─ .env (任意)             # 環境変数ファイル（.gitignore で除外）
│
├─ .gitignore                  # ルート配置の .gitignore
├─ README.md                   # このファイル
└─ LICENSE (任意)             # ライセンスファイル
```

- **backend/app.py**  
  - Flask アプリ本体。`/api/messages` にアクセスすると JSON が返る。  
  - 自動リロードを有効にするため、最後に `app.run(debug=True)` が書かれています。  

- **backend/requirements.txt**  
  - Flask や CORS、ORM などバックエンドに必要なパッケージを列挙。  
  - 新しいパッケージを追加する際はここに追記し、`pip install -r requirements.txt` を再実行します。  

- **frontend/src/**  
  - React コンポーネントや CSS などを格納。`App.js` がエントリーポイントです。  

- **frontend/package.json**  
  - `react`、`react-dom`、`react-scripts` などの依存を列挙。  
  - `npm install <package> --save` を実行すると自動でここに追記されます。  

- **.gitignore**  
  - `backend/__pycache__/` や `*.db`、`frontend/node_modules/`、キャッシュファイルなどを除外する設定が書かれています。  

## Gitフック (`post-merge`) の利用

複数人開発で便利な Git の自動化機能として、`git pull` の後に依存パッケージのインストールを自動化する方法があります。

### 設定手順

1. `.git/hooks/` ディレクトリに移動し、`post-merge` というファイルを作成します：

```bash
cd .git/hooks
touch post-merge
chmod +x post-merge
```

2. 以下のようにスクリプトを記述します：

```bash
#!/bin/bash

echo "🔄 frontend npm install 実行中..."
cd frontend
[ -f package.json ] && npm install

echo "🔄 backend requirements.txt 実行中..."
cd ../backend
[ -f requirements.txt ] && pip install -r requirements.txt

echo "✅ 自動セットアップ完了"
```

> ⚠ `.git/hooks/` 以下は Git によって共有されないため、チームメンバー各自でこのスクリプトを作成・設置する必要があります。
> 共有したい場合は、`scripts/setup.sh` のように共通スクリプト化して管理することもおすすめです。

---

## ライセンス

特に指定がない場合は任意のオープンソースライセンス（例：MIT License）を適用してください。  
必要であれば `LICENSE` ファイルを追加して明示してください。

// frontend/src/App.js
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import { AuthRoutes } from "./routes/AuthRoutes";
import { UserRoutes } from "./routes/UserRoutes";
import { CommunityRoutes } from "./routes/CommunityRoutes";

// 今後、別ページを追加したい場合はここにインポートして
// import About from "./pages/About";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ホーム画面 (メッセージ一覧) */}
        <Route path="/" element={<Home />} />

        {/* 各機能用のルーティング */}
        {AuthRoutes}
        {UserRoutes}
        {CommunityRoutes}
      </Routes>
    </BrowserRouter>
  );
}

// frontend/src/App.js
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import AppLayout from "./AppLayout";

import { AuthRoutes } from "./routes/AuthRoutes";
import { UserRoutes } from "./routes/UserRoutes";
import { CommunityRoutes } from "./routes/CommunityRoutes";

// 今後、別ページを追加したい場合はここにインポートして
// import About from "./pages/About";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* 共通レイアウトに包むルート */}
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Home />} />
          {/* 他のページルートもここにネスト */}
          {UserRoutes}
          {CommunityRoutes}
        </Route>

        {/* ログインページなど、レイアウト不要なルート */}
        {AuthRoutes}
      </Routes>
    </BrowserRouter>
  );
}
// frontend/src/App.js
import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Header from "./components/Header";
import CommunityLeave from "./components/CommunityLeave";
import Home from "./pages/Home";

// 今後、別ページを追加したい場合はここにインポートして
// import About from "./pages/About";

export default function App() {
  return (
    <BrowserRouter>
      <Header />

      <Routes>
        {/* ホーム画面 (メッセージ一覧) */}
        <Route path="/" element={<Home />} />

        {/* 例：他のページを追加する場合
        <Route path="/about" element={<About />} />
        */}
        <Route path="/community/leave" element={<CommunityLeave />} />
        {/* どのパスにもマッチしない場合は Home に飛ばす */}
        <Route path="*" element={<Home />} />
      </Routes>
    </BrowserRouter>
  );
}

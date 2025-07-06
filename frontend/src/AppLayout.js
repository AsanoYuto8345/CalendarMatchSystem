// src/routes/AppLayout.js
import { useState } from "react";
import { Outlet } from "react-router-dom";

import HamburgerMenu from "./components/HambergerMenuUI"; // ハンバーガーメニューコンポーネント

export default function AppLayout() {
  const [selectedCommunityId, setSelectedCommunityId] = useState("");

  return (
    <>
      <HamburgerMenu selectedCommunityId={selectedCommunityId} setSelectedCommunityId={setSelectedCommunityId}/>
      <main>
        <Outlet /> {/* 各ページがここに差し込まれる */}
      </main>
    </>
  );
}
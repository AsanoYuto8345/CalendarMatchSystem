// src/routes/AppLayout.js
import { Outlet } from "react-router-dom";
import HamburgerMenu from "./components/HambergerMenuUI"; // ハンバーガーメニューコンポーネント

export default function AppLayout() {
  return (
    <>
      <HamburgerMenu />
      <main>
        <Outlet /> {/* 各ページがここに差し込まれる */}
      </main>
    </>
  );
}
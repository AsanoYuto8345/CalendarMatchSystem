// frontend/src/components/Header.js
import React from "react";
import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header style={{ background: "#f4f4f4", padding: "10px 20px" }}>
      <nav>
        <Link to="/" style={{ marginRight: 15 }}>Home</Link>
        {/* 今後もし別ページが増えたらここに Link を追加できる */}
      </nav>
    </header>
  );
}

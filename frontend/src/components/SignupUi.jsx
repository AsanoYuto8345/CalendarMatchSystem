import React, { useState } from "react";

const SignupUI = () => {
  return (
    <div className="signup-container" style={{ maxWidth: "400px", margin: "0 auto", padding: "20px" }}>
      <h2>サインアップ</h2>
      
      <div className="form-group" style={{ marginBottom: "15px" }}>
        <label>メールアドレス</label>
        <input type="text" name="email" className="form-control" placeholder="メールアドレスを入力" />
        <small>半角英数（50文字以内）</small>
      </div>

      <div className="form-group" style={{ marginBottom: "15px" }}>
        <label>パスワード</label>
        <input type="password" name="pw" className="form-control" placeholder="パスワードを入力" />
        <small>半角英数（20文字以内）</small>
      </div>

      <div className="form-group" style={{ marginBottom: "15px" }}>
        <label>表示名</label>
        <input type="text" name="name" className="form-control" placeholder="表示名を入力" />
        <small>半角英数（20文字以内）</small>
      </div>

      <div className="form-group" style={{ marginBottom: "15px" }}>
        <label>アイコン画像</label><br />
        <input type="file" name="icon_name" accept="image/*" />
        <small>画像データ（サイズ制限）</small>
      </div>

      <button type="submit" className="btn btn-primary">サインアップ</button>
    </div>
  );
};

export default SignupUI;
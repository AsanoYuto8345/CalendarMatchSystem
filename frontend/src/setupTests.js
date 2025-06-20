// src/setupTests.js

// TextEncoder のポリフィルを追加
// Jestのjsdom環境でTextEncoderが未定義の場合に必要
// Node.jsの 'util' モジュールから TextEncoder をインポートしてグローバルに設定します。
if (typeof global.TextEncoder === 'undefined') {
  const { TextEncoder } = require('util');
  global.TextEncoder = TextEncoder;
}


// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom'; 
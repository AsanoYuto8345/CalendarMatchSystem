// CalendarMatchSystem/frontend/src/components/SignupUI.test.jsx
// SignupUIコンポーネントの単体テスト
// 担当: 石田めぐみ 

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import SignupUI from './SignupUI'; // テスト対象のコンポーネントをインポート

describe('SignupUI', () => {
  // --- 要素の表示確認テスト ---

  test('「サインアップ」タイトルと各入力フィールド、ボタンが正しく表示されること', () => {
    // コンポーネントをレンダリング（onSubmitClick と msg はダミー関数/空文字列でOK）
    render(<SignupUI onSubmitClick={() => {}} msg="" />);

    // タイトルが表示されていることを確認
    expect(screen.getByText('サインアップ')).toBeInTheDocument();

    // 各ラベルと入力フィールドが表示されていることを確認
    expect(screen.getByLabelText('メールアドレス')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('example@example.com')).toBeInTheDocument();

    expect(screen.getByLabelText('パスワード')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('パスワード')).toBeInTheDocument();

    expect(screen.getByLabelText('表示名')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('表示名')).toBeInTheDocument();

    expect(screen.getByLabelText('アイコン画像')).toBeInTheDocument();
    expect(screen.getByText('画像ファイルを選択してください')).toBeInTheDocument(); // smallタグのテキスト

    // サインアップボタンが表示されていることを確認 (getByRole 'button' を使うのがより頑健)
    expect(screen.getByRole('button', { name: /サインアップ/i })).toBeInTheDocument();
  });

  test('msgプロパティが渡されたときに結果メッセージが表示されること', () => {
    const testMessage = 'テストメッセージです';
    render(<SignupUI onSubmitClick={() => {}} msg={testMessage} />);

    // 表示されたメッセージがドキュメント内にあることを確認
    expect(screen.getByText(testMessage)).toBeInTheDocument();
    // メッセージが赤色のテキストであることを確認 (Tailwind CSSクラスの確認)
    const messageElement = screen.getByText(testMessage);
    expect(messageElement).toHaveClass('text-red-500'); // haveClassは@testing-library/jest-domのマッチャー
  });

  test('msgプロパティが空の場合、結果メッセージが表示されないこと', () => {
    render(<SignupUI onSubmitClick={() => {}} msg="" />);

    // テストメッセージが存在しないことを確認
    // queryByTextは要素が存在しない場合にnullを返すため、エラーにならない
    expect(screen.queryByText(/テストメッセージ/)).not.toBeInTheDocument();
    // もしメッセージの特定の一部が表示されることがあれば、それを指定
    expect(screen.queryByText('アカウントを作成しました')).not.toBeInTheDocument();
    expect(screen.queryByText('作成に失敗しました。もう一度お試しください。')).not.toBeInTheDocument();
  });


  // --- ユーザーインタラクションテスト ---

  test('「サインアップ」ボタンがクリックされたときにonSubmitClick関数が呼ばれること', () => {
    // モック関数を作成
    const mockOnSubmitClick = jest.fn();

    // コンポーネントをレンダリングし、onSubmitClickにモック関数を渡す
    render(<SignupUI onSubmitClick={mockOnSubmitClick} msg="" />);

    // サインアップボタンを取得
    const signupButton = screen.getByRole('button', { name: /サインアップ/i });

    // ボタンをクリック
    fireEvent.click(signupButton);

    // mockOnSubmitClick関数が1回呼ばれたことを確認
    expect(mockOnSubmitClick).toHaveBeenCalledTimes(1);
  });

  test('onSubmitClick関数が渡されない場合でもボタンクリックでエラーにならないこと', () => {
    // onSubmitClickを渡さないでレンダリング
    render(<SignupUI msg="" />);

    const signupButton = screen.getByRole('button', { name: /サインアップ/i });

    // ボタンをクリックしてもエラーが発生しないことを確認（テストが正常終了すること）
    fireEvent.click(signupButton);
    // 特にエラーがないことをアサートする特別な方法はないが、テストがパスすること自体が成功の証
  });
});
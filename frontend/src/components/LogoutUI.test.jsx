// CalendarMatchSystem/frontend/src/components/LogoutUI.test.jsx
// LogoutUIコンポーネントの単体テスト (Jest対応版)
// 担当: 石田めぐみ

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event'; // userEvent は Jest 環境でも利用可能
import LogoutUI from './LogoutUI';

describe('LogoutUI', () => {
  // テストのセットアップとして、userEventを初期化
  const user = userEvent.setup();

  // --- 要素の表示確認テスト ---

  it('「ログアウト」タイトルと確認メッセージ、ボタンが正しく表示されること', () => {
    // コンポーネントをレンダリングし、モック関数を渡す
    render(<LogoutUI onAcceptClick={() => {}} onRejectClick={() => {}} />);

    // タイトルが表示されていることを確認 (getByRole 'heading' を使用)
    expect(screen.getByRole('heading', { name: /ログアウト/i, level: 2 })).toBeInTheDocument();
    // 確認メッセージが表示されていることを確認
    expect(screen.getByText('ログアウトしますか？')).toBeInTheDocument();

    // 「はい」ボタンと「いいえ」ボタンが表示されていることを確認
    expect(screen.getByRole('button', { name: 'はい' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'いいえ' })).toBeInTheDocument();
  });

  // --- ユーザーインタラクションテスト ---

  it('「はい」ボタンがクリックされたときにonAcceptClick関数が呼ばれること', async () => {
    // onAcceptClickとonRejectClickのモック関数を作成
    // JestのAPIである jest.fn() を使用
    const handleAcceptClick = jest.fn();
    const handleRejectClick = jest.fn();

    // コンポーネントをレンダリングし、モック関数を渡す
    render(
      <LogoutUI
        onAcceptClick={handleAcceptClick}
        onRejectClick={handleRejectClick}
      />
    );

    // 「はい」ボタンを取得し、クリックイベントをシミュレート
    const acceptButton = screen.getByRole('button', { name: 'はい' });
    await user.click(acceptButton);

    // handleAcceptClick が1回だけ呼び出されたことを確認
    expect(handleAcceptClick).toHaveBeenCalledTimes(1);
    // handleRejectClick は呼び出されていないことを確認
    expect(handleRejectClick).not.toHaveBeenCalled();
  });

  it('「いいえ」ボタンがクリックされたときにonRejectClick関数が呼ばれること', async () => {
    // onAcceptClickとonRejectClickのモック関数を作成
    // JestのAPIである jest.fn() を使用
    const handleAcceptClick = jest.fn();
    const handleRejectClick = jest.fn();

    // コンポーネントをレンダリングし、モック関数を渡す
    render(
      <LogoutUI
        onAcceptClick={handleAcceptClick}
        onRejectClick={handleRejectClick}
      />
    );

    // 「いいえ」ボタンを取得し、クリックイベントをシミュレート
    const rejectButton = screen.getByRole('button', { name: 'いいえ' });
    await user.click(rejectButton);

    // handleRejectClick が1回だけ呼び出されたことを確認
    expect(handleRejectClick).toHaveBeenCalledTimes(1);
    // handleAcceptClick は呼び出されていないことを確認
    expect(handleAcceptClick).not.toHaveBeenCalled();
  });

  it('クリックハンドラが渡されない場合でもボタンクリックでエラーにならないこと', async () => {
    // onAcceptClickとonRejectClickを渡さないでレンダリング
    render(<LogoutUI />); 

    // 「はい」ボタンと「いいえ」ボタンを取得
    const acceptButton = screen.getByRole('button', { name: 'はい' });
    const rejectButton = screen.getByRole('button', { name: 'いいえ' });

    // ボタンをクリックしてもエラーが発生しないことを確認
    await user.click(acceptButton);
    await user.click(rejectButton);

    // テストがエラーなく完了すること自体が、エラーが発生しないことの証明です。
  });
});
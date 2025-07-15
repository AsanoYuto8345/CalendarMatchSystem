// W20 ユーザ情報編集完了Mに対応するReactコンポーネント 担当: 角田一颯

import { useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';

const UserInfoEditM = () => {
  const navigate = useNavigate();
  const timerRef = useRef(null);

  useEffect(() => {
    timerRef.current = setTimeout(() => {
      navigate('/');
    }, 3000);

    return () => clearTimeout(timerRef.current);
  }, [navigate]);

  const handleClose = () => {
    clearTimeout(timerRef.current);  // タイマー解除
    navigate('/');       // 即遷移
  };

  return (
    <div className="max-w-md mx-auto mt-16 p-6 bg-white shadow-lg rounded-lg relative">
      <button
        onClick={handleClose}
        className="absolute top-2 right-2 text-gray-500 hover:text-gray-700"
        aria-label="閉じる"
      >
        ×
      </button>
      <h2 className="text-2xl font-bold text-center mb-4">編集完了</h2>
      <p className="text-center text-lg text-green-700">ユーザ情報を更新しました。</p>
    </div>
  );
};

export default UserInfoEditM;

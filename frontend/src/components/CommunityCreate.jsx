// src/components/CommunityCreate.jsx

/**
 * コミュニティ作成画面 UIコンポーネント
 * 作成者: 遠藤 信輝
 */

import React, { useState } from 'react';

/**
 * CommunityCreate コンポーネント
 * コミュニティ名と画像を送信して新規作成を行う
 */
function CommunityCreate() {
  const [communityName, setCommunityName] = useState('');
  const [image, setImage] = useState(null);
  const [message, setMessage] = useState('');
  const [preview, setPreview] = useState('');
  const [loading, setLoading] = useState(false);
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  // 選択された画像ファイルの処理とプレビュー表示
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    if (file) setPreview(URL.createObjectURL(file));
  };

  // コミュニティ作成のフォーム送信処理
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    if (!communityName.trim()) {
      setMessage('コミュニティ名を入力してください');
      setLoading(false);
      return;
    }
    if (communityName.length > 16) {
      setMessage('コミュニティ名は16文字以内で入力してください');
      setLoading(false);
      return;
    }

    try {
      const formData = new FormData();
      formData.append('community_name', communityName);
      if (image) formData.append('image', image);

      const response = await fetch('http://localhost:5001/community/create', {
        method: 'POST',
        body: formData
      });

      const text = await response.text();
      let data;
      try { data = JSON.parse(text); } catch {
        setMessage(`サーバーエラー: レスポンスがJSONではありません (${response.status})`);
        return;
      }

      if (response.ok) {
        setShowSuccessModal(true);
        const name = data.community_name || communityName;
        setMessage(`コミュニティ「${name}」を作成しました！`);
        setCommunityName('');
        setImage(null);
        setPreview('');
        const fileInput = document.getElementById('image-upload');
        if (fileInput) fileInput.value = '';
      } else {
        setMessage(data.error || `エラーが発生しました (${response.status})`);
      }
    } catch (err) {
      setMessage(`送信エラー: ${err.message}`);
    }

    setLoading(false);
  };

  return (
    <div className="p-5 max-w-xl mx-auto">
      {showSuccessModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-8 rounded-lg relative min-w-[300px] text-center shadow-lg">
            <button
              onClick={() => setShowSuccessModal(false)}
              className="absolute top-2 right-2 text-xl text-gray-500 hover:text-black"
            >×</button>
            <h3 className="mt-4 text-lg font-semibold">作成完了</h3>
          </div>
        </div>
      )}

      <h2 className="text-xl font-bold mb-4">コミュニティ作成</h2>

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label className="block mb-1 font-medium">コミュニティ名：</label>
          <input
            type="text"
            value={communityName}
            onChange={(e) => setCommunityName(e.target.value)}
            maxLength={16}
            required
            className="w-full p-2 border border-gray-300 rounded"
          />
          <small className="text-gray-500">{communityName.length}/16文字</small>
        </div>

        <div className="mb-4">
          <label htmlFor="image-upload" className="cursor-pointer text-blue-600 underline">
            📷 画像を選ぶ（任意）
          </label>
          <input
            id="image-upload"
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            className="hidden"
          />
          {image && <div className="mt-2 text-sm text-gray-600">選択された画像: {image.name} ({Math.round(image.size/1024)}KB)</div>}
        </div>

        {preview && (
          <div className="mb-4">
            <img src={preview} alt="preview" className="w-24 h-24 object-cover border border-gray-300 rounded" />
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-2 px-4 rounded text-white ${loading ? 'bg-gray-500 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
        >{loading ? '作成中...' : '作成'}</button>
      </form>

      {message && (
        <div className={`mt-4 p-3 rounded text-sm border ${message.includes('エラー')||message.includes('失敗') ? 'bg-red-100 text-red-800 border-red-300' : 'bg-green-100 text-green-800 border-green-300'}`}>
          {message}
        </div>
      )}
    </div>
  );
}

export default CommunityCreate;

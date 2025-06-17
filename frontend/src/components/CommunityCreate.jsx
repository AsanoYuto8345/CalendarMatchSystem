/**
 * コミュニティ作成画面
 * 作成者: 遠藤　信輝
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

  /** 
   * 選択された画像ファイルの処理とプレビュー表示
   */
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    if (file) {
      setPreview(URL.createObjectURL(file));
    }
  };

  /**
   * コミュニティ作成のフォーム送信処理
   */
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
      if (image) {
        formData.append('image', image);
      }

      const response = await fetch('http://localhost:5001/community/create', {
        method: 'POST',
        body: formData
      });

      const responseText = await response.text();
      let data;
      try {
        data = JSON.parse(responseText);
      } catch {
        setMessage(`サーバーエラー: レスポンスがJSONではありません (${response.status})`);
        return;
      }

      if (response.ok) {
        setShowSuccessModal(true);
        setMessage(data.message || '作成に成功しました！');
        setCommunityName('');
        setImage(null);
        setPreview('');
        const fileInput = document.getElementById('image-upload');
        if (fileInput) fileInput.value = '';
      } else {
        setMessage(data.error || `エラーが発生しました (${response.status})`);
      }
    } catch (error) {
      setMessage(`送信エラー: ${error.message}`);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '500px' }}>
      {showSuccessModal && (
        <div
          style={{
            position: 'fixed',
            top: '0',
            left: '0',
            width: '100vw',
            height: '100vh',
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            zIndex: '1000'
          }}
        >
          <div
            style={{
              backgroundColor: 'white',
              padding: '30px 40px',
              borderRadius: '8px',
              position: 'relative',
              minWidth: '300px',
              textAlign: 'center',
              boxShadow: '0 4px 12px rgba(0,0,0,0.2)'
            }}
          >
            <button
              onClick={() => setShowSuccessModal(false)}
              style={{
                position: 'absolute',
                top: '10px',
                right: '10px',
                background: 'transparent',
                border: 'none',
                fontSize: '20px',
                cursor: 'pointer'
              }}
            >
              ×
            </button>
            <h3 style={{ marginTop: '20px', fontSize: '20px' }}>作成完了</h3>
          </div>
        </div>
      )}

      <h2>コミュニティ作成</h2>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label style={{ display: 'block', marginBottom: '5px' }}>
            コミュニティ名：
          </label>
          <input
            type="text"
            value={communityName}
            onChange={(e) => setCommunityName(e.target.value)}
            maxLength={16}
            required
            style={{
              width: '100%',
              padding: '8px',
              border: '1px solid #ddd',
              borderRadius: '4px'
            }}
          />
          <small style={{ color: '#666' }}>
            {communityName.length}/16文字
          </small>
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label
            htmlFor="image-upload"
            style={{
              cursor: 'pointer',
              color: '#007bff',
              textDecoration: 'underline'
            }}
          >
            📷 画像を選ぶ（任意）
          </label>
          <input
            id="image-upload"
            type="file"
            accept="image/*"
            onChange={handleImageChange}
            style={{ display: 'none' }}
          />
          {image && (
            <div style={{ marginTop: '8px', fontSize: '14px', color: '#666' }}>
              選択された画像: {image.name} ({Math.round(image.size / 1024)}KB)
            </div>
          )}
        </div>

        {preview && (
          <div style={{ marginBottom: '15px' }}>
            <img
              src={preview}
              alt="preview"
              style={{
                width: '100px',
                height: '100px',
                objectFit: 'cover',
                border: '1px solid #ddd',
                borderRadius: '4px'
              }}
            />
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '10px 20px',
            backgroundColor: loading ? '#6c757d' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            width: '100%'
          }}
        >
          {loading ? '作成中...' : '作成'}
        </button>
      </form>

      {message && (
        <div
          style={{
            marginTop: '15px',
            padding: '10px',
            backgroundColor:
              message.includes('エラー') || message.includes('失敗')
                ? '#f8d7da'
                : '#d4edda',
            color:
              message.includes('エラー') || message.includes('失敗')
                ? '#721c24'
                : '#155724',
            border: `1px solid ${
              message.includes('エラー') || message.includes('失敗')
                ? '#f5c6cb'
                : '#c3e6cb'
            }`,
            borderRadius: '4px',
            fontSize: '14px'
          }}
        >
          {message}
        </div>
      )}
    </div>
  );
}

export default CommunityCreate;

/**
 * M3 コミュニティ参加画面
 * 作成者: 遠藤　信輝
 */

import React, { useState } from 'react';
import { FaCamera } from 'react-icons/fa';
import axios from 'axios';

/**
 * CommunityJoin
 * ユーザがコミュニティ名を入力し参加する画面
 */
function CommunityJoin() {
  const [communityId, setCommunityId] = useState('');
  const [showSuccessModal, setShowSuccessModal] = useState(false);

  /**
   * コミュニティ参加リクエスト送信
   */
  const handleJoin = async (e) => {
    e.preventDefault();

    try {
      await axios.post('http://localhost:5001/community/join', {
        community_name: communityId
      });

      setShowSuccessModal(true);
    } catch (error) {
      alert(
        error.response?.data?.error ||
        error.response?.data?.message ||
        error.message ||
        'サーバエラーが発生しました'
      );
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: '#f8f8f8'
      }}
    >
      {/* 成功モーダル */}
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
            <h3 style={{ marginTop: '20px', fontSize: '20px' }}>参加完了</h3>
          </div>
        </div>
      )}

      <form
        onSubmit={handleJoin}
        style={{
          backgroundColor: 'white',
          padding: '40px',
          borderRadius: '8px',
          boxShadow: '0 0 10px rgba(0,0,0,0.1)',
          width: '320px',
          textAlign: 'center'
        }}
      >
        <h2 style={{ marginBottom: '30px' }}>コミュニティ参加</h2>

        <div
          style={{
            width: '80px',
            height: '80px',
            borderRadius: '50%',
            border: '2px solid #ccc',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            margin: '0 auto 30px'
          }}
        >
          <FaCamera size={28} color="#888" />
        </div>

        <input
          type="text"
          placeholder="コミュニティ名"
          value={communityId}
          onChange={(e) => setCommunityId(e.target.value)}
          required
          style={{
            width: '100%',
            padding: '10px',
            marginBottom: '20px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          }}
        />

        <button
          type="submit"
          style={{
            padding: '10px 20px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            width: '100%',
            cursor: 'pointer'
          }}
        >
          参加する
        </button>
      </form>
    </div>
  );
}

export default CommunityJoin;

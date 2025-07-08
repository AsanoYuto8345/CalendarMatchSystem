import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';

function App() {
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';">
      <div className="text-center">
        <h1 className="text-7xl font-extrabold text-blue-600">CalendarMatchingSystem</h1>
        <p className="mt-6 text-3xl text-gray-700">05班</p>
        <button
          onClick={() => navigate('/auth/signup')}
          className="mt-10 px-6 py-3 bg-blue-500 text-white text-xl rounded hover:bg-blue-600"
        >
          サインアップ
        </button>
      </div>
    </div>
  );
}

export default App;

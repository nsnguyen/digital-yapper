import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import TestEndpoint from './pages/TestEndpoint';
import ChatPage from './pages/ChatPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between">
              <h1 className="text-3xl font-bold text-gray-900">Digital Yapper</h1>
              <nav className="flex space-x-4">
                <a href="/" className="text-blue-600 hover:text-blue-800">Home</a>
                <a href="/chat" className="text-blue-600 hover:text-blue-800">Chat</a>
                <a href="/test_endpoint" className="text-blue-600 hover:text-blue-800">Test API</a>
              </nav>
            </div>
          </div>
        </header>
        <main>
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <div className="px-4 py-6 sm:px-0">
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/chat" element={<ChatPage />} />
                <Route path="/test_endpoint" element={<TestEndpoint />} />
              </Routes>
            </div>
          </div>
        </main>
        <footer className="bg-white shadow-inner mt-auto">
          <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 text-center text-gray-500">
            <p>Digital Yapper - Nursing Assistant &copy; {new Date().getFullYear()}</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;

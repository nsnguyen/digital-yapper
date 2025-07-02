import React from 'react';
import NursingChat from '../components/NursingChat';

function ChatPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-6">
      <div className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Nursing Assistant
          </h1>
          <p className="text-lg text-gray-600">
            Ask questions about nursing policies and procedures
          </p>
        </div>
        
        <NursingChat />
        
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-500">
            Demo system - Always verify with official hospital policies
          </p>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;

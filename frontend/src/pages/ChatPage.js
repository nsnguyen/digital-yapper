import React from 'react';
import NursingChat from '../components/NursingChat';

function ChatPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Nursing Assistant
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Ask questions about nursing policies and procedures. 
            Just tell me your unit and role to get started.
          </p>
        </div>
        
        <NursingChat />
        
        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500">
            Demo system - Always verify with official hospital policies
          </p>
        </div>
      </div>
    </div>
  );
}

export default ChatPage;

import React, { useState, useRef, useEffect } from "react";
import { sendStreamingChatMessage } from "../services/api";

function NursingChat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Hi! I am your nursing assistant. To provide the most accurate policy information, please tell me your role (e.g., Nurse, Tech) and which unit you work in (e.g., ICU, ED).",
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setIsLoading(true);

    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);

    let assistantContent = "";
    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: "", isStreaming: true },
    ]);

    try {
      const resultConversationId = await sendStreamingChatMessage(
        userMessage,
        conversationId,
        (chunk) => {
          assistantContent += chunk;
          setMessages((prev) => {
            const newMessages = [...prev];
            const lastMessage = newMessages[newMessages.length - 1];
            if (lastMessage.role === "assistant") {
              lastMessage.content = assistantContent;
            }
            return newMessages;
          });
        },
      );

      if (resultConversationId) {
        setConversationId(resultConversationId);
      }

      setMessages((prev) => {
        const newMessages = [...prev];
        const lastMessage = newMessages[newMessages.length - 1];
        if (lastMessage.role === "assistant") {
          lastMessage.isStreaming = false;
        }
        return newMessages;
      });
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = {
          role: "assistant",
          content: "Sorry, I encountered an error. Please try again.",
          isStreaming: false,
        };
        return newMessages;
      });
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: "assistant",
        content:
          "Hi! I am your nursing assistant. To provide the most accurate policy information, please tell me your role (e.g., Nurse, Tech) and which unit you work in (e.g., ICU, ED).",
      },
    ]);
    setConversationId(null);
    inputRef.current?.focus();
  };

  return (
    <div className="flex flex-col h-[700px] max-w-5xl mx-auto border border-gray-300 rounded-lg bg-white shadow-lg">
      <div className="flex items-center justify-between p-4 border-b border-gray-200 bg-blue-50">
        <h2 className="text-xl font-semibold text-gray-800">
          Digital Yapper - Nursing Assistant
        </h2>
        <button
          onClick={clearChat}
          className="px-3 py-1 text-sm text-blue-600 border border-blue-600 rounded hover:bg-blue-50"
        >
          New Chat
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={
              message.role === "user"
                ? "flex justify-end"
                : "flex justify-start"
            }
          >
            <div
              className={
                message.role === "user"
                  ? "max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-blue-500 text-white"
                  : "max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-gray-100 text-gray-800 border"
              }
            >
              <div className="whitespace-pre-wrap">
                {message.content}
                {message.isStreaming && (
                  <span className="inline-block w-2 h-5 bg-gray-400 ml-1 animate-pulse" />
                )}
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about nursing policies..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
            autoFocus
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className={
              isLoading || !input.trim()
                ? "px-6 py-2 rounded-md text-white font-medium bg-gray-400 cursor-not-allowed"
                : "px-6 py-2 rounded-md text-white font-medium bg-blue-500 hover:bg-blue-600"
            }
          >
            {isLoading ? "Sending..." : "Send"}
          </button>
        </div>
      </form>

      <div className="px-4 pb-3 text-xs text-gray-500">
        <div className="flex flex-wrap gap-2">
          <span className="font-medium">Try:</span>
          <button
            onClick={() => setInput("Hi, I am a nurse in ICU")}
            className="hover:text-blue-600 cursor-pointer"
          >
            Hi, I am a nurse in ICU
          </button>
          <span>•</span>
          <button
            onClick={() => setInput("How do I clean IV lines?")}
            className="hover:text-blue-600 cursor-pointer"
          >
            How do I clean IV lines?
          </button>
        </div>
      </div>
    </div>
  );
}

export default NursingChat;

import React, { useState, useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';
import ChatInput from './ChatInput';
import { Message } from '../types/chat';

interface ChatWindowProps {
  user_id: string;
  initialMessages?: Message[];
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  conversationId: number | null;
}

const ChatWindow: React.FC<ChatWindowProps> = ({
  user_id,
  initialMessages = [],
  onSendMessage,
  isLoading,
  conversationId
}) => {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    setMessages(initialMessages);
  }, [initialMessages]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleSend = (text: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    onSendMessage(text);
  };

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Message list */}
      <div className="flex-1 overflow-y-auto p-3 md:p-4 space-y-4 scrollbar-thin scrollbar-thumb-blue-200 dark:scrollbar-thumb-slate-600 scrollbar-track-transparent">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center py-6 px-3">
            <div className="max-w-md w-full break-words">
              <div className="mb-6 p-5 bg-gradient-to-br from-blue-100/80 to-indigo-100/80 dark:from-slate-700/80 dark:to-slate-600/80 rounded-2xl shadow-lg backdrop-blur-sm border border-white/20 dark:border-slate-600/30">
                <div className="bg-gradient-to-r from-blue-500 to-indigo-600 p-3 rounded-xl inline-block mb-4 flex-shrink-0">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-10 w-10 text-white"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                    />
                  </svg>
                </div>

                <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-3 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent break-words">
                  Welcome to Todo AI Chatbot
                </h2>

                <p className="text-base text-gray-600 dark:text-gray-300 leading-relaxed mb-4 break-words">
                  Start a conversation by typing a message below. I can help manage your todos with AI assistance.
                </p>

                <div className="items-center justify-center space-x-2 text-xs text-gray-500 dark:text-gray-400 bg-gray-100/50 dark:bg-slate-700/50 px-3 py-1.5 rounded-full inline-flex">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse flex-shrink-0"></div>
                  <span>AI Assistant Ready</span>
                </div>

                {conversationId && (
                  <p className="text-sm text-gray-500 dark:text-gray-500 mt-6 bg-gray-100/50 dark:bg-slate-700/50 px-4 py-2 rounded-full font-mono break-words">
                    Conversation ID: <span className="font-bold">#{conversationId}</span>
                  </p>
                )}
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div key={message.id} className="fade-in" style={{ animationDelay: `${index * 40}ms` }}>
                <MessageBubble
                  role={message.role}
                  content={message.content}
                  timestamp={message.timestamp}
                />
              </div>
            ))}

            {isLoading && <div className="fade-in"><TypingIndicator /></div>}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input bar */}
      <div className="border-t border-gray-200/50 dark:border-slate-700/50 bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm p-3 shadow-xl shrink-0">
        <ChatInput onSend={handleSend} disabled={isLoading} />
      </div>
    </div>
  );
};

export default ChatWindow;
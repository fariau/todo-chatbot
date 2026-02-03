'use client';

import { useState, useEffect, useRef } from 'react';
import ChatWindow from '../components/ChatWindow';
import { sendMessage } from '../lib/api';
import { Message } from '../types/chat';

function ChatWrapper() {
  const [user_id, setUser_id] = useState<string>('testuser');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isMounted, setIsMounted] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null); // For auto-scroll (optional enhancement)

  useEffect(() => {
    setIsMounted(true);

    const savedMessages = localStorage.getItem('chat_messages');
    if (savedMessages) {
      try {
        const parsed = JSON.parse(savedMessages);
        const loadedMessages = parsed.map((msg: any) => ({
          ...msg,
          timestamp: new Date(msg.timestamp)
        }));
        setMessages(loadedMessages);
      } catch (e) {
        console.error('Error parsing saved messages:', e);
      }
    }

    const savedId = localStorage.getItem('conversation_id');
    if (savedId) {
      setConversationId(parseInt(savedId, 10));
    }
  }, []);

  useEffect(() => {
    if (isMounted) {
      localStorage.setItem('chat_messages', JSON.stringify(messages));
    }
  }, [messages, isMounted]);

  useEffect(() => {
    if (isMounted) {
      if (conversationId !== null) {
        localStorage.setItem('conversation_id', conversationId.toString());
      } else {
        localStorage.removeItem('conversation_id');
      }
    }
  }, [conversationId, isMounted]);

  const handleSendMessage = async (message: string) => {
    setIsLoading(true);
    try {
      const response = await sendMessage(user_id, message, conversationId ?? undefined);

      const userMessage: Message = {
        id: Date.now().toString(),
        role: 'user',
        content: message,
        timestamp: new Date()
      };

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      };

      if (response.conversation_id && response.conversation_id !== conversationId) {
        setConversationId(response.conversation_id);
      }

      setMessages(prev => [...prev, userMessage, assistantMessage]);
    } catch (error: any) {
      console.error('Error sending message:', error);
      let errorMessageText = 'Sorry, I encountered an error processing your request. Please try again.';
      if (error?.response?.data?.detail) {
        errorMessageText = error.response.data.detail;
      } else if (error?.message) {
        errorMessageText = error.message;
      }
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: errorMessageText,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
    setConversationId(null);
    localStorage.removeItem('chat_messages');
    localStorage.removeItem('conversation_id');
  };

  if (!isMounted) {
    return (
      <div className="h-dvh flex flex-col bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-slate-900 dark:to-slate-800 overflow-hidden">
        {/* Loading placeholder – keep as is or simplify */}
        <div className="flex-1 flex items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-dvh flex flex-col overflow-hidden bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-slate-900 dark:to-slate-800">
      {/* Header – sticky top */}
      <header className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white p-4 shadow-xl backdrop-blur-sm bg-opacity-95 sticky top-0 z-50 border-b border-white/10 w-full">
        <div className="container mx-auto flex flex-col sm:flex-row justify-between items-center gap-4 max-w-full">
          <div className="flex items-center min-w-0 flex-1">
            <div className="bg-white/20 p-2 rounded-xl mr-3 flex-shrink-0">
              {/* Your icon */}
              <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold tracking-tight whitespace-nowrap overflow-hidden text-ellipsis min-w-0 flex-1">Todo AI Chatbot</h1>
          </div>
          <div className="flex items-center space-x-3 flex-shrink-0">
            <div className="bg-blue-700/30 px-4 py-2 rounded-xl flex items-center max-w-[150px]">
              <div className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse flex-shrink-0"></div>
              <span className="text-sm font-medium whitespace-nowrap overflow-hidden text-ellipsis">Chatting as {user_id}</span>
            </div>
            <button
              onClick={clearChat}
              className="bg-red-500/80 hover:bg-red-600/90 px-4 py-2 rounded-xl transition-all duration-200 flex items-center group shadow-lg hover:shadow-xl whitespace-nowrap flex-shrink-0"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
              <span className="font-medium">Clear Chat</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main – takes remaining space, no page scroll */}
      <main className="flex-1 overflow-hidden w-full">
        <ChatWindow
          user_id={user_id}
          initialMessages={messages}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
          conversationId={conversationId}
        />
      </main>
    </div>
  );
}

export default function HomePage() {
  return <ChatWrapper />;
}
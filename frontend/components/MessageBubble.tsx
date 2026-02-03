import React from 'react';
import { format } from 'date-fns';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date | string;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ role, content, timestamp }) => {
  const isUser = role === 'user';

  // Generate initials for avatar
  const getInitials = (role: string) => {
    if (isUser) return 'U';
    return 'AI';
  };

  // Simple markdown rendering without external libraries to avoid hydration issues
  const renderMarkdown = (text: string) => {
    // Convert basic markdown elements to HTML
    let html = text
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-semibold">$1</strong>') // Bold
      .replace(/\*(.*?)\*/g, '<em class="italic">$1</em>') // Italic
      .replace(/~~(.*?)~~/g, '<del class="line-through">$1</del>') // Strikethrough
      .replace(/`(.*?)`/g, '<code class="bg-gray-100 dark:bg-slate-700/80 px-2 py-1 rounded-md text-sm font-mono border border-gray-200 dark:border-slate-600">$1</code>') // Inline code
      .replace(/^### (.*$)/gm, '<h3 class="font-semibold text-lg mt-4 mb-2 text-gray-800 dark:text-gray-200">$1</h3>') // H3
      .replace(/^## (.*$)/gm, '<h2 class="font-semibold text-xl mt-5 mb-3 text-gray-800 dark:text-gray-200">$1</h2>') // H2
      .replace(/^# (.*$)/gm, '<h1 class="font-bold text-2xl mt-6 mb-4 text-gray-800 dark:text-gray-200">$1</h1>') // H1
      .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" class="text-blue-600 dark:text-blue-400 underline hover:text-blue-800 dark:hover:text-blue-300 transition-colors font-medium" target="_blank" rel="noopener noreferrer">$1</a>') // Links
      .replace(/\n/g, '<br />'); // Line breaks

    return { __html: html };
  };

  // Convert timestamp to Date object if it's a string
  const timestampDate = typeof timestamp === 'string' ? new Date(timestamp) : timestamp;

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-6`}>
      <div className="flex items-start space-x-3 max-w-[85%] sm:max-w-[80%] md:max-w-[70%] lg:max-w-[60%]">
        {/* Avatar */}
        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center shadow-lg ${
          isUser
            ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
            : 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white'
        }`}>
          <span className="text-sm font-bold">{getInitials(role)}</span>
        </div>

        {/* Message bubble */}
        <div
          className={`px-5 py-4 rounded-2xl shadow-lg transition-all duration-200 hover:shadow-xl ${
            isUser
              ? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-br-none ml-auto'
              : 'bg-white dark:bg-slate-700/90 text-gray-800 dark:text-gray-200 border border-gray-200/50 dark:border-slate-600/50 rounded-bl-none backdrop-blur-sm'
          }`}
        >
          <div
            className="whitespace-pre-wrap break-words prose prose-sm max-w-none text-base leading-relaxed"
            dangerouslySetInnerHTML={renderMarkdown(content)}
          />
          <div className={`text-xs mt-3 ${isUser ? 'text-blue-100/80' : 'text-gray-500 dark:text-gray-400'} text-right font-mono`}>
            {format(timestampDate, 'HH:mm')}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;
import React from 'react';

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex justify-start mb-4 fade-in">
      <div className="flex items-end space-x-2 max-w-[60%]">
        <div className="flex-shrink-0 w-9 h-9 rounded-full flex items-center justify-center bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-sm">
          <span className="text-xs font-semibold">AI</span>
        </div>
        <div className="bg-white dark:bg-slate-700 text-gray-800 dark:text-gray-200 px-4 py-3 rounded-2xl shadow-sm border border-gray-200 dark:border-slate-600 rounded-bl-none">
          <div className="flex space-x-1.5">
            <div className="w-2 h-2 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full bounce"></div>
            <div className="w-2 h-2 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full bounce delay-75"></div>
            <div className="w-2 h-2 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full bounce delay-150"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TypingIndicator;
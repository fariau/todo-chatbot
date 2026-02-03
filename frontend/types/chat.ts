export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date | string;
}

export interface ToolCall {
  name: string;
  arguments: Record<string, any>;
  result: Record<string, any>;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: ToolCall[];
}
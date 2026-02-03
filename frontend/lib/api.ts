import axios from 'axios';
import { ChatResponse, Message } from '../types/chat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const sendMessage = async (
  user_id: string,
  message: string,
  conversation_id?: number
): Promise<ChatResponse> => {
  try {
    const response = await api.post(`/api/${user_id}/chat`, {
      message,
      conversation_id: conversation_id || null,
    });

    return response.data;
  } catch (error: any) {
    console.error('Error sending message:', error);

    // Handle specific error responses from the backend
    if (error.response?.data?.detail) {
      // Re-throw with the detailed error message from backend
      const errorDetail = error.response.data.detail;

      // Create a mock response with the error as the AI response
      throw {
        response: errorDetail,
        conversation_id: conversation_id || null,
        tool_calls: []
      };
    }

    throw error;
  }
};
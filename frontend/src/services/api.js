import axios from 'axios';

// Create an axios instance with defaults
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Submit data to the API
 * @param {Object} data - Data to submit
 * @returns {Promise} - Promise with API response
 */
export const submitData = async (data) => {
  try {
    const response = await api.post('/api/data/submit', data);
    return response.data;
  } catch (error) {
    console.error('Error submitting data:', error);
    throw new Error(
      error.response?.data?.detail || 
      'Failed to submit data to API'
    );
  }
};

/**
 * Fetch data from the API
 * @returns {Promise} - Promise with fetched data
 */
export const fetchData = async () => {
  try {
    const response = await api.get('/api/data');
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw new Error(
      error.response?.data?.detail || 
      'Failed to fetch data from API'
    );
  }
};

/**
 * Get server status information
 * @returns {Promise} - Promise with server info
 */
export const getServerInfo = async () => {
  try {
    const response = await api.get('/api/status');
    return response.data;
  } catch (error) {
    console.error('Error getting server info:', error);
    throw new Error(
      error.response?.data?.detail || 
      'Failed to get server information'
    );
  }
};

/**
 * Send a chat message (non-streaming)
 * @param {string} content - Message content
 * @param {string} conversationId - Optional conversation ID
 * @returns {Promise} - Promise with chat response
 */
export const sendChatMessage = async (content, conversationId = null) => {
  try {
    const response = await api.post('/api/chat/', {
      content,
      conversation_id: conversationId
    });
    return response.data;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw new Error(
      error.response?.data?.detail || 
      'Failed to send chat message'
    );
  }
};

/**
 * Send a streaming chat message
 * @param {string} content - Message content
 * @param {string} conversationId - Optional conversation ID
 * @param {function} onChunk - Callback for each chunk
 * @returns {Promise} - Promise that resolves when stream completes
 */
export const sendStreamingChatMessage = async (content, conversationId = null, onChunk) => {
  try {
    const response = await fetch(`${api.defaults.baseURL}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content,
        conversation_id: conversationId
      })
    });

    if (!response.ok) {
      throw new Error('Failed to start chat stream');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let conversationIdFromStream = null;

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // Keep incomplete line in buffer

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.content) {
                onChunk(data.content);
              }
              if (data.conversation_id) {
                conversationIdFromStream = data.conversation_id;
              }
              if (data.type === 'done') {
                return conversationIdFromStream;
              }
            } catch (e) {
              // If it's not JSON, treat as plain text
              const content = line.slice(6);
              if (content.trim()) {
                onChunk(content);
              }
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }

    return conversationIdFromStream;
  } catch (error) {
    console.error('Error with streaming chat:', error);
    throw new Error('Failed to send streaming chat message');
  }
};

/**
 * Get conversation history
 * @returns {Promise} - Promise with conversations list
 */
export const getConversations = async () => {
  try {
    const response = await api.get('/api/chat/conversations');
    return response.data;
  } catch (error) {
    console.error('Error fetching conversations:', error);
    throw new Error('Failed to fetch conversations');
  }
};

/**
 * Get messages for a specific conversation
 * @param {string} conversationId - Conversation ID
 * @returns {Promise} - Promise with messages list
 */
export const getConversationMessages = async (conversationId) => {
  try {
    const response = await api.get(`/api/chat/conversations/${conversationId}/messages`);
    return response.data;
  } catch (error) {
    console.error('Error fetching conversation messages:', error);
    throw new Error('Failed to fetch conversation messages');
  }
};

export default api;

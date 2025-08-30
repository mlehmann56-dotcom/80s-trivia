import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Session management
export const getSessionId = () => {
  let sessionId = localStorage.getItem('80s-trivia-session-id');
  if (!sessionId) {
    sessionId = generateSessionId();
    localStorage.setItem('80s-trivia-session-id', sessionId);
  }
  return sessionId;
};

const generateSessionId = () => {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

// Questions API
export const getQuestions = async (level, category) => {
  try {
    const response = await axios.get(`${API_BASE}/questions/${level}/${category}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching questions:', error);
    throw error;
  }
};

export const getRandomQuestions = async (level, category, count) => {
  try {
    const response = await axios.get(`${API_BASE}/questions/random/${level}/${category}/${count}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching random questions:', error);
    throw error;
  }
};

export const getQuestionsStats = async () => {
  try {
    const response = await axios.get(`${API_BASE}/questions/stats`);
    return response.data;
  } catch (error) {
    console.error('Error fetching questions stats:', error);
    throw error;
  }
};

// User Progress API
export const getUserProgress = async (sessionId) => {
  try {
    const response = await axios.get(`${API_BASE}/user/progress/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user progress:', error);
    throw error;
  }
};

export const updateUserProgress = async (progressData) => {
  try {
    const response = await axios.post(`${API_BASE}/user/progress`, progressData);
    return response.data;
  } catch (error) {
    console.error('Error updating user progress:', error);
    throw error;
  }
};

export const getLevelProgressSummary = async (sessionId) => {
  try {
    const response = await axios.get(`${API_BASE}/user/levels/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching level progress summary:', error);
    throw error;
  }
};

export const checkLevelUnlockStatus = async (level, sessionId) => {
  try {
    const response = await axios.get(`${API_BASE}/user/levels/${level}/unlock-status/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('Error checking level unlock status:', error);
    throw error;
  }
};

export const getLeaderboard = async (limit = 10) => {
  try {
    const response = await axios.get(`${API_BASE}/user/leaderboard?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching leaderboard:', error);
    throw error;
  }
};

// Error handling wrapper
export const withErrorHandling = async (apiCall, fallbackData = null) => {
  try {
    return await apiCall();
  } catch (error) {
    console.error('API call failed:', error);
    
    // Return fallback data if available
    if (fallbackData !== null) {
      return fallbackData;
    }
    
    // Rethrow error if no fallback
    throw error;
  }
};
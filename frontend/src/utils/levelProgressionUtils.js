import { getUserProgress, updateUserProgress, getSessionId } from '../services/apiService';

// Level progression utility functions
export const calculateScore = (correctAnswers, totalQuestions) => {
  return Math.round((correctAnswers / totalQuestions) * 100);
};

export const isLevelUnlocked = (level, userData) => {
  if (level === 1) return true;
  
  const previousLevel = level - 1;
  const previousLevelData = userData.levels[previousLevel.toString()];
  
  if (!previousLevelData) return false;
  
  // Check if all categories in previous level have been completed with 80%+ score
  const categories = ['music', 'movies', 'fashion', 'general'];
  return categories.every(category => {
    const categoryData = previousLevelData[category];
    return categoryData && categoryData.completed && categoryData.score >= 80;
  });
};

export const getOverallLevelProgress = (level, userData) => {
  const levelData = userData.levels[level.toString()];
  if (!levelData) return { completed: 0, total: 4, percentage: 0 };
  
  const categories = ['music', 'movies', 'fashion', 'general'];
  const completed = categories.filter(category => {
    const categoryData = levelData[category];
    return categoryData && categoryData.completed && categoryData.score >= 80;
  }).length;
  
  return {
    completed,
    total: 4,
    percentage: Math.round((completed / 4) * 100)
  };
};

export const getNextUnlockedLevel = (userData) => {
  for (let level = 1; level <= 10; level++) {
    if (isLevelUnlocked(level, userData)) {
      const progress = getOverallLevelProgress(level, userData);
      if (progress.completed < 4) {
        return level;
      }
    } else {
      return level - 1; // Return last unlocked level
    }
  }
  return 10; // All levels completed
};

export const initializeUserData = async () => {
  try {
    const sessionId = getSessionId();
    const userData = await getUserProgress(sessionId);
    return userData;
  } catch (error) {
    console.error('Error initializing user data:', error);
    // Return default structure if API fails
    return {
      sessionId: getSessionId(),
      levels: {},
      currentLevel: 1,
      totalQuestionsAnswered: 0,
      totalCorrectAnswers: 0,
      averageScore: 0.0
    };
  }
};

export const saveUserProgress = async (progressData) => {
  try {
    const sessionId = getSessionId();
    const updatedProgress = await updateUserProgress({
      sessionId,
      ...progressData
    });
    return updatedProgress;
  } catch (error) {
    console.error('Error saving user progress:', error);
    throw error;
  }
};

export const updateCategoryProgress = async (userData, level, category, score, totalQuestions, answers) => {
  try {
    const sessionId = getSessionId();
    const progressData = {
      sessionId,
      level,
      category,
      score: calculateScore(score, totalQuestions),
      totalQuestions,
      answers: answers || []
    };
    
    const updatedProgress = await updateUserProgress(progressData);
    return updatedProgress;
  } catch (error) {
    console.error('Error updating category progress:', error);
    throw error;
  }
};
// Level progression utility functions
export const calculateScore = (correctAnswers, totalQuestions) => {
  return Math.round((correctAnswers / totalQuestions) * 100);
};

export const isLevelUnlocked = (level, userData) => {
  if (level === 1) return true;
  
  const previousLevel = level - 1;
  const previousLevelData = userData.levels[previousLevel];
  
  if (!previousLevelData) return false;
  
  // Check if all categories in previous level have been completed with 80%+ score
  const categories = ['music', 'movies', 'fashion', 'general'];
  return categories.every(category => {
    const categoryData = previousLevelData[category];
    return categoryData && categoryData.completed && categoryData.score >= 80;
  });
};

export const getOverallLevelProgress = (level, userData) => {
  const levelData = userData.levels[level];
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

export const initializeUserData = () => {
  const savedData = localStorage.getItem('80s-trivia-progress');
  if (savedData) {
    return JSON.parse(savedData);
  }
  
  return {
    currentLevel: 1,
    levels: {}
  };
};

export const saveUserProgress = (userData) => {
  localStorage.setItem('80s-trivia-progress', JSON.stringify(userData));
};

export const updateCategoryProgress = (userData, level, category, score, totalQuestions) => {
  if (!userData.levels[level]) {
    userData.levels[level] = {};
  }
  
  userData.levels[level][category] = {
    score: calculateScore(score, totalQuestions),
    completed: true,
    completedAt: new Date().toISOString()
  };
  
  saveUserProgress(userData);
  return userData;
};
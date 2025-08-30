import React, { useState, useEffect } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import LevelSelector from "./components/LevelSelector";
import CategorySelector from "./components/CategorySelector";
import QuizPage from "./components/QuizPage";
import ResultsPage from "./components/ResultsPage";
import { Toaster } from "./components/ui/toaster";
import { initializeUserData } from "./utils/levelProgressionUtils";

function App() {
  const [userData, setUserData] = useState(null);
  const [currentLevel, setCurrentLevel] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load user data on app start
    const loadUserData = async () => {
      try {
        const initialUserData = await initializeUserData();
        setUserData(initialUserData);
      } catch (error) {
        console.error('Failed to load user data:', error);
        // Set fallback data
        setUserData({
          sessionId: `fallback_${Date.now()}`,
          levels: {},
          currentLevel: 1,
          totalQuestionsAnswered: 0,
          totalCorrectAnswers: 0,
          averageScore: 0.0
        });
      } finally {
        setLoading(false);
      }
    };

    loadUserData();
  }, []);

  if (loading) {
    return (
      <div className="App min-h-screen bg-gradient-to-br from-purple-900 via-pink-800 to-indigo-900 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🎵</div>
          <div className="text-white text-2xl">Loading 80s Trivia...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="App min-h-screen bg-gradient-to-br from-purple-900 via-pink-800 to-indigo-900">
      <BrowserRouter>
        <Routes>
          <Route 
            path="/" 
            element={
              <LevelSelector 
                userData={userData} 
                setCurrentLevel={setCurrentLevel}
              />
            } 
          />
          <Route 
            path="/categories" 
            element={
              <CategorySelector 
                currentLevel={currentLevel}
                userData={userData}
                setCurrentLevel={setCurrentLevel}
              />
            } 
          />
          <Route 
            path="/quiz/:category" 
            element={
              <QuizPage 
                currentLevel={currentLevel}
                userData={userData}
                setUserData={setUserData}
              />
            } 
          />
          <Route 
            path="/results" 
            element={<ResultsPage currentLevel={currentLevel} />} 
          />
        </Routes>
        <Toaster />
      </BrowserRouter>
    </div>
  );
}

export default App;
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
  const [userData, setUserData] = useState(initializeUserData());
  const [currentLevel, setCurrentLevel] = useState(1);

  useEffect(() => {
    // Load user data on app start
    const savedUserData = initializeUserData();
    setUserData(savedUserData);
  }, []);

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
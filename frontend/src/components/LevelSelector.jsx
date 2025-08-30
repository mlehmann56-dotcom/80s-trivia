import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Progress } from "./ui/progress";
import { Lock, Star, Trophy, CheckCircle } from "lucide-react";
import { levelInfo } from "../data/mockQuestionsLevels";
import { isLevelUnlocked, getOverallLevelProgress } from "../utils/levelProgressionUtils";

const LevelSelector = ({ userData, setCurrentLevel }) => {
  const navigate = useNavigate();

  const handleLevelSelect = (level) => {
    if (isLevelUnlocked(level, userData)) {
      setCurrentLevel(level);
      navigate("/categories");
    }
  };

  const getLevelColor = (level) => {
    const colors = [
      "from-pink-500 to-purple-600",
      "from-cyan-500 to-blue-600", 
      "from-yellow-500 to-orange-600",
      "from-green-500 to-teal-600",
      "from-red-500 to-pink-600",
      "from-indigo-500 to-purple-600",
      "from-orange-500 to-red-600",
      "from-teal-500 to-green-600",
      "from-purple-500 to-indigo-600",
      "from-yellow-400 to-orange-500"
    ];
    return colors[level - 1] || colors[0];
  };

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-pink-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent mb-4">
            CHOOSE YOUR LEVEL
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Progress through 10 levels of increasingly challenging 80s trivia. Achieve 80% in all categories to unlock the next level!
          </p>
        </div>

        {/* Levels Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {Object.entries(levelInfo).map(([level, info]) => {
            const levelNum = parseInt(level);
            const unlocked = isLevelUnlocked(levelNum, userData);
            const progress = getOverallLevelProgress(levelNum, userData);
            const isCompleted = progress.completed === 4;
            
            return (
              <Card 
                key={level}
                className={`${unlocked ? 'bg-black/30 border-gray-700 hover:border-gray-500 cursor-pointer' : 'bg-gray-800/50 border-gray-800'} 
                  transition-all duration-300 transform ${unlocked ? 'hover:scale-105' : ''} backdrop-blur-sm`}
                onClick={() => unlocked && handleLevelSelect(levelNum)}
              >
                <CardHeader className="text-center">
                  <div className={`w-16 h-16 mx-auto mb-4 rounded-full ${unlocked ? `bg-gradient-to-r ${getLevelColor(levelNum)}` : 'bg-gray-600'} 
                    flex items-center justify-center text-white shadow-lg`}>
                    {!unlocked ? (
                      <Lock className="w-8 h-8" />
                    ) : isCompleted ? (
                      <Trophy className="w-8 h-8" />
                    ) : (
                      <Star className="w-8 h-8" />
                    )}
                  </div>
                  
                  <div className="flex items-center justify-center gap-2 mb-2">
                    <CardTitle className={`text-xl ${unlocked ? 'text-white' : 'text-gray-500'}`}>
                      Level {level}
                    </CardTitle>
                    {isCompleted && <CheckCircle className="w-5 h-5 text-green-400" />}
                  </div>
                  
                  <Badge variant={unlocked ? "default" : "secondary"} className="mx-auto">
                    {info.name}
                  </Badge>
                </CardHeader>
                
                <CardContent className="text-center">
                  <p className={`${unlocked ? 'text-gray-300' : 'text-gray-500'} mb-4 text-sm`}>
                    {info.description}
                  </p>
                  
                  {unlocked && (
                    <div className="mb-4">
                      <div className="flex justify-between text-sm text-gray-400 mb-2">
                        <span>Progress</span>
                        <span>{progress.completed}/4 categories</span>
                      </div>
                      <Progress value={progress.percentage} className="h-2" />
                    </div>
                  )}
                  
                  <Button 
                    className={`w-full ${unlocked ? `bg-gradient-to-r ${getLevelColor(levelNum)} text-white font-semibold py-2` : 'bg-gray-600 text-gray-400 cursor-not-allowed'} 
                      transition-all duration-300`}
                    disabled={!unlocked}
                  >
                    {!unlocked ? 'Locked' : isCompleted ? 'Replay Level' : 'Enter Level'}
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Progress Summary */}
        <div className="mt-12 text-center bg-black/20 rounded-xl p-8 backdrop-blur-sm border border-gray-700">
          <h2 className="text-2xl font-bold text-white mb-4">Your Journey</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div>
              <div className="text-3xl font-bold text-cyan-400">
                {Object.keys(userData.levels || {}).length}
              </div>
              <div className="text-gray-300">Levels Started</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-400">
                {Object.values(userData.levels || {}).filter(level => 
                  Object.values(level).filter(cat => cat.completed && cat.score >= 80).length === 4
                ).length}
              </div>
              <div className="text-gray-300">Levels Completed</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-purple-400">
                {Object.values(userData.levels || {}).reduce((total, level) => 
                  total + Object.values(level).filter(cat => cat.completed).length, 0
                )}
              </div>
              <div className="text-gray-300">Categories Completed</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-yellow-400">
                {Math.round(Object.values(userData.levels || {}).reduce((total, level) => {
                  const scores = Object.values(level).filter(cat => cat.completed).map(cat => cat.score);
                  return total + (scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0);
                }, 0) / Math.max(Object.keys(userData.levels || {}).length, 1))}%
              </div>
              <div className="text-gray-300">Average Score</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LevelSelector;
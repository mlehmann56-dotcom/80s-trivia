import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Music, Film, Shirt, Star, ArrowLeft, CheckCircle } from "lucide-react";
import { levelInfo } from "../data/mockQuestionsLevels";

const CategorySelector = ({ currentLevel, userData, setCurrentLevel }) => {
  const navigate = useNavigate();

  const categories = [
    {
      id: "music",
      title: "Music",
      description: "Test your knowledge of 80s hits, bands, and musical legends",
      icon: <Music className="w-8 h-8" />,
      color: "from-pink-500 to-purple-600",
      hoverColor: "hover:from-pink-600 hover:to-purple-700"
    },
    {
      id: "movies",
      title: "Movies", 
      description: "Iconic films, actors, and memorable moments from the decade",
      icon: <Film className="w-8 h-8" />,
      color: "from-cyan-500 to-blue-600",
      hoverColor: "hover:from-cyan-600 hover:to-blue-700"
    },
    {
      id: "fashion",
      title: "Fashion",
      description: "Big hair, bold colors, and the trends that defined the era",
      icon: <Shirt className="w-8 h-8" />,
      color: "from-yellow-500 to-orange-600", 
      hoverColor: "hover:from-yellow-600 hover:to-orange-700"
    },
    {
      id: "general",
      title: "General Knowledge",
      description: "Politics, technology, and cultural events of the 1980s",
      icon: <Star className="w-8 h-8" />,
      color: "from-green-500 to-teal-600",
      hoverColor: "hover:from-green-600 hover:to-teal-700"
    }
  ];

  const handleCategorySelect = (categoryId) => {
    navigate(`/quiz/${categoryId}`);
  };

  const handleBackToLevels = () => {
    navigate("/");
  };

  const getCategoryProgress = (categoryId) => {
    const levelData = userData.levels[currentLevel];
    if (!levelData || !levelData[categoryId]) {
      return { completed: false, score: 0 };
    }
    return levelData[categoryId];
  };

  const currentLevelInfo = levelInfo[currentLevel];

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Button
            variant="outline"
            onClick={handleBackToLevels}
            className="bg-black/30 border-gray-600 text-white hover:bg-black/50"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Levels
          </Button>
          
          <div className="text-center">
            <Badge variant="default" className="mb-2 text-lg px-4 py-1">
              Level {currentLevel}
            </Badge>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-pink-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
              {currentLevelInfo.name}
            </h1>
            <p className="text-gray-300 mt-2">{currentLevelInfo.description}</p>
          </div>
          
          <div className="w-32"></div> {/* Spacer for centering */}
        </div>

        {/* Level Progress */}
        <div className="text-center mb-8 bg-black/20 rounded-xl p-6 backdrop-blur-sm border border-gray-700">
          <h2 className="text-xl font-bold text-white mb-4">Complete all categories with 80%+ to unlock the next level!</h2>
          <div className="flex justify-center gap-8">
            {categories.map((category) => {
              const progress = getCategoryProgress(category.id);
              return (
                <div key={category.id} className="text-center">
                  <div className={`w-12 h-12 mx-auto mb-2 rounded-full bg-gradient-to-r ${category.color} flex items-center justify-center text-white relative`}>
                    {category.icon}
                    {progress.completed && progress.score >= 80 && (
                      <CheckCircle className="w-4 h-4 absolute -top-1 -right-1 bg-green-500 rounded-full text-white" />
                    )}
                  </div>
                  <div className="text-sm text-gray-300">{category.title}</div>
                  {progress.completed && (
                    <div className={`text-sm font-semibold ${progress.score >= 80 ? 'text-green-400' : 'text-yellow-400'}`}>
                      {progress.score}%
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {categories.map((category) => {
            const progress = getCategoryProgress(category.id);
            
            return (
              <Card 
                key={category.id}
                className="bg-black/30 border-gray-700 hover:border-gray-500 transition-all duration-300 transform hover:scale-105 cursor-pointer backdrop-blur-sm"
                onClick={() => handleCategorySelect(category.id)}
              >
                <CardHeader className="text-center">
                  <div className={`w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-r ${category.color} flex items-center justify-center text-white shadow-lg relative`}>
                    {category.icon}
                    {progress.completed && progress.score >= 80 && (
                      <CheckCircle className="w-6 h-6 absolute -top-2 -right-2 bg-green-500 rounded-full text-white p-1" />
                    )}
                  </div>
                  <CardTitle className="text-2xl text-white">{category.title}</CardTitle>
                  {progress.completed && (
                    <Badge variant={progress.score >= 80 ? "default" : "secondary"} className="mx-auto">
                      Completed: {progress.score}%
                    </Badge>
                  )}
                </CardHeader>
                <CardContent className="text-center">
                  <p className="text-gray-300 mb-6">{category.description}</p>
                  <Button 
                    className={`w-full bg-gradient-to-r ${category.color} ${category.hoverColor} text-white font-semibold py-3 transition-all duration-300 shadow-lg hover:shadow-xl`}
                  >
                    {progress.completed ? 'Retake Quiz' : 'Start Quiz'}
                  </Button>
                </CardContent>
              </Card>
            );
          })}
        </div>

        {/* Level Info */}
        <div className="text-center bg-black/20 rounded-xl p-8 backdrop-blur-sm border border-gray-700">
          <h2 className="text-2xl font-bold text-white mb-4">Level {currentLevel} Challenge</h2>
          <p className="text-gray-300 text-lg">
            {currentLevel === 1 && "Welcome to the 80s! Start with these classic questions covering the most iconic moments of the decade."}
            {currentLevel === 2 && "Ready for deeper cuts? These questions require more specialized 80s knowledge."}
            {currentLevel >= 3 && `Expert level ${currentLevel}! Only true 80s scholars will master these ultra-challenging questions.`}
          </p>
        </div>
      </div>
    </div>
  );
};

export default CategorySelector;
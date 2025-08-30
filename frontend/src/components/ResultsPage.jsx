import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Trophy, Star, RefreshCw, Home, Award, ArrowRight, Lock } from "lucide-react";

const ResultsPage = ({ currentLevel }) => {
  const location = useLocation();
  const navigate = useNavigate();
  
  const { 
    score = 0, 
    totalQuestions = 0, 
    category = "Quiz",
    level = 1,
    levelName = "Rad Rookie"
  } = location.state || {};
  
  const percentage = Math.round((score / totalQuestions) * 100);
  const passedLevel = percentage >= 80;

  const getPerformanceLevel = () => {
    if (percentage >= 90) return { level: "Totally Awesome!", color: "from-yellow-400 to-orange-500", icon: <Trophy className="w-12 h-12" /> };
    if (percentage >= 80) return { level: "Radical!", color: "from-green-400 to-blue-500", icon: <Award className="w-12 h-12" /> };
    if (percentage >= 70) return { level: "Pretty Cool!", color: "from-blue-400 to-purple-500", icon: <Star className="w-12 h-12" /> };
    if (percentage >= 60) return { level: "Not Bad!", color: "from-purple-400 to-pink-500", icon: <Star className="w-12 h-12" /> };
    return { level: "Keep Trying!", color: "from-gray-400 to-gray-600", icon: <RefreshCw className="w-12 h-12" /> };
  };

  const performance = getPerformanceLevel();

  const handleRetryQuiz = () => {
    navigate(`/quiz/${category.toLowerCase()}`);
  };

  const handleGoHome = () => {
    navigate("/categories");
  };

  const handleNextLevel = () => {
    navigate("/");
  };

  const getCategoryColor = () => {
    switch (category.toLowerCase()) {
      case "music": return "from-pink-500 to-purple-600";
      case "movies": return "from-cyan-500 to-blue-600";
      case "fashion": return "from-yellow-500 to-orange-600";
      case "general": return "from-green-500 to-teal-600";
      default: return "from-pink-500 to-purple-600";
    }
  };

  return (
    <div className="min-h-screen p-6 flex items-center justify-center">
      <div className="max-w-2xl w-full">
        {/* Results Card */}
        <Card className="bg-black/30 border-gray-700 backdrop-blur-sm text-center">
          <CardHeader className="pb-4">
            <div className="flex justify-center gap-2 mb-4">
              <Badge variant="default">Level {level}</Badge>
              <Badge variant="secondary">{levelName}</Badge>
            </div>
            <div className={`w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-r ${performance.color} flex items-center justify-center text-white shadow-xl`}>
              {performance.icon}
            </div>
            <CardTitle className="text-4xl text-white mb-2">
              Quiz Complete!
            </CardTitle>
            <p className={`text-2xl font-bold bg-gradient-to-r ${getCategoryColor()} bg-clip-text text-transparent`}>
              {category} Trivia
            </p>
          </CardHeader>
          
          <CardContent className="space-y-8">
            {/* Score Display */}
            <div className="space-y-4">
              <div className="text-6xl font-bold text-white">
                {score}<span className="text-3xl text-gray-400">/{totalQuestions}</span>
              </div>
              <div className={`text-3xl font-bold bg-gradient-to-r ${performance.color} bg-clip-text text-transparent`}>
                {percentage}%
              </div>
              <p className={`text-xl font-semibold bg-gradient-to-r ${performance.color} bg-clip-text text-transparent`}>
                {performance.level}
              </p>
            </div>

            {/* Performance Message */}
            <div className="bg-black/20 rounded-lg p-6 border border-gray-700">
              <p className="text-gray-300 text-lg mb-4">
                {percentage >= 90 && "You're a true 80s expert! Totally tubular performance!"}
                {percentage >= 80 && percentage < 90 && "Excellent knowledge of the 80s! You really know your stuff!"}
                {percentage >= 70 && percentage < 80 && "Good job! You've got solid 80s knowledge!"}
                {percentage >= 60 && percentage < 70 && "Not bad! Keep exploring the awesome 80s!"}
                {percentage < 60 && "The 80s were an amazing decade - keep learning about this radical era!"}
              </p>
              
              {/* Level Progression Message */}
              {passedLevel ? (
                <div className="bg-green-900/50 border border-green-700 rounded-lg p-4">
                  <p className="text-green-300 font-semibold">
                    🎉 Congratulations! You passed this category with {percentage}%!
                  </p>
                  <p className="text-green-400 text-sm mt-1">
                    Complete all 4 categories with 80%+ to unlock the next level!
                  </p>
                </div>
              ) : (
                <div className="bg-yellow-900/50 border border-yellow-700 rounded-lg p-4">
                  <p className="text-yellow-300 font-semibold">
                    You need 80% or higher to pass this level.
                  </p>
                  <p className="text-yellow-400 text-sm mt-1">
                    Try again to unlock the next level!
                  </p>
                </div>
              )}
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Button
                onClick={handleRetryQuiz}
                className={`flex-1 bg-gradient-to-r ${getCategoryColor()} text-white py-3 text-lg font-semibold hover:shadow-xl transition-all duration-300`}
              >
                <RefreshCw className="w-5 h-5 mr-2" />
                Try Again
              </Button>
              <Button
                onClick={handleGoHome}
                variant="outline"
                className="flex-1 bg-black/30 border-gray-600 text-white hover:bg-black/50 py-3 text-lg"
              >
                <Home className="w-5 h-5 mr-2" />
                Choose Category
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Fun Fact */}
        <div className="mt-8 text-center bg-black/20 rounded-xl p-6 backdrop-blur-sm border border-gray-700">
          <h3 className="text-xl font-bold text-white mb-2">80s Fun Fact!</h3>
          <p className="text-gray-300">
            {category.toLowerCase() === "music" && "The 80s saw the birth of MTV with 'Video Killed the Radio Star' as the first music video!"}
            {category.toLowerCase() === "movies" && "The 80s gave us some of the highest-grossing films of all time, including E.T. and the Star Wars sequels!"}
            {category.toLowerCase() === "fashion" && "Shoulder pads were so popular in the 80s that they became a symbol of power dressing!"}
            {category.toLowerCase() === "general" && "The 80s introduced us to personal computers, video games, and the beginning of the digital age!"}
            {!["music", "movies", "fashion", "general"].includes(category.toLowerCase()) && "The 1980s were known as the 'Decade of Excess' for their bold style and innovations!"}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;
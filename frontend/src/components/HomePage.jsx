import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Music, Film, Shirt, Star, Zap, Headphones } from "lucide-react";

const HomePage = () => {
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

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-6">
            <Zap className="w-12 h-12 text-yellow-400" />
            <h1 className="text-6xl font-bold bg-gradient-to-r from-pink-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
              80s TRIVIA
            </h1>
            <Headphones className="w-12 h-12 text-pink-400" />
          </div>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Take a radical trip back to the most awesome decade! Test your knowledge of 80s music, movies, fashion, and culture.
          </p>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
          {categories.map((category) => (
            <Card 
              key={category.id} 
              className="bg-black/30 border-gray-700 hover:border-gray-500 transition-all duration-300 transform hover:scale-105 cursor-pointer backdrop-blur-sm"
              onClick={() => handleCategorySelect(category.id)}
            >
              <CardHeader className="text-center">
                <div className={`w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-r ${category.color} flex items-center justify-center text-white shadow-lg`}>
                  {category.icon}
                </div>
                <CardTitle className="text-2xl text-white">{category.title}</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-gray-300 mb-6">{category.description}</p>
                <Button 
                  className={`w-full bg-gradient-to-r ${category.color} ${category.hoverColor} text-white font-semibold py-3 transition-all duration-300 shadow-lg hover:shadow-xl`}
                >
                  Start Quiz
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Fun Facts */}
        <div className="text-center bg-black/20 rounded-xl p-8 backdrop-blur-sm border border-gray-700">
          <h2 className="text-2xl font-bold text-white mb-4">Did You Know?</h2>
          <p className="text-gray-300 text-lg">
            The 1980s gave us MTV, the first mobile phone, Pac-Man, and some of the most iconic movies and music of all time!
          </p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
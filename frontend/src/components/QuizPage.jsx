import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Progress } from "./ui/progress";
import { mockQuestions } from "../data/mockQuestions";
import { CheckCircle, XCircle, ArrowLeft, Clock } from "lucide-react";
import { useToast } from "../hooks/use-toast";

const QuizPage = () => {
  const { category } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();
  
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(30);
  const [quizCompleted, setQuizCompleted] = useState(false);

  useEffect(() => {
    if (mockQuestions[category]) {
      setQuestions(mockQuestions[category]);
    } else {
      navigate("/");
    }
  }, [category, navigate]);

  useEffect(() => {
    if (timeLeft > 0 && !showResult && !quizCompleted) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    } else if (timeLeft === 0 && !showResult) {
      handleNextQuestion();
    }
  }, [timeLeft, showResult, quizCompleted]);

  const currentQuestion = questions[currentQuestionIndex];

  const handleAnswerSelect = (answerIndex) => {
    if (selectedAnswer !== null || showResult) return;
    
    setSelectedAnswer(answerIndex);
    setShowResult(true);
    
    if (answerIndex === currentQuestion.correctAnswer) {
      setScore(score + 1);
      toast({
        title: "Correct! 🎉",
        description: "Totally rad answer!",
      });
    } else {
      toast({
        title: "Not quite! 😅",
        description: `The correct answer was: ${currentQuestion.options[currentQuestion.correctAnswer]}`,
        variant: "destructive",
      });
    }
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedAnswer(null);
      setShowResult(false);
      setTimeLeft(30);
    } else {
      setQuizCompleted(true);
      navigate("/results", { 
        state: { 
          score, 
          totalQuestions: questions.length, 
          category: category.charAt(0).toUpperCase() + category.slice(1) 
        } 
      });
    }
  };

  const handleGoBack = () => {
    navigate("/");
  };

  const getCategoryColor = () => {
    switch (category) {
      case "music": return "from-pink-500 to-purple-600";
      case "movies": return "from-cyan-500 to-blue-600";
      case "fashion": return "from-yellow-500 to-orange-600";
      case "general": return "from-green-500 to-teal-600";
      default: return "from-pink-500 to-purple-600";
    }
  };

  if (!currentQuestion) {
    return <div className="min-h-screen flex items-center justify-center text-white">Loading...</div>;
  }

  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

  return (
    <div className="min-h-screen p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <Button
            variant="outline"
            onClick={handleGoBack}
            className="bg-black/30 border-gray-600 text-white hover:bg-black/50"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Categories
          </Button>
          
          <div className="text-center">
            <h1 className={`text-3xl font-bold bg-gradient-to-r ${getCategoryColor()} bg-clip-text text-transparent`}>
              {category.charAt(0).toUpperCase() + category.slice(1)} Quiz
            </h1>
            <p className="text-gray-300">
              Question {currentQuestionIndex + 1} of {questions.length}
            </p>
          </div>
          
          <div className="flex items-center gap-2 text-white">
            <Clock className="w-5 h-5" />
            <span className={`text-xl font-bold ${timeLeft <= 10 ? 'text-red-400' : 'text-white'}`}>
              {timeLeft}s
            </span>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <Progress value={progress} className="h-3" />
        </div>

        {/* Question Card */}
        <Card className="bg-black/30 border-gray-700 backdrop-blur-sm mb-8">
          <CardHeader>
            <CardTitle className="text-2xl text-white text-center">
              {currentQuestion.question}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 gap-4">
              {currentQuestion.options.map((option, index) => {
                let buttonClass = "bg-gray-800 hover:bg-gray-700 text-white border-gray-600 p-4 text-left justify-start h-auto";
                
                if (showResult) {
                  if (index === currentQuestion.correctAnswer) {
                    buttonClass = "bg-green-600 text-white border-green-500 p-4 text-left justify-start h-auto";
                  } else if (index === selectedAnswer && index !== currentQuestion.correctAnswer) {
                    buttonClass = "bg-red-600 text-white border-red-500 p-4 text-left justify-start h-auto";
                  } else {
                    buttonClass = "bg-gray-600 text-gray-300 border-gray-500 p-4 text-left justify-start h-auto";
                  }
                }

                return (
                  <Button
                    key={index}
                    variant="outline"
                    className={`${buttonClass} transition-all duration-300 transform hover:scale-105`}
                    onClick={() => handleAnswerSelect(index)}
                    disabled={showResult}
                  >
                    <div className="flex items-center justify-between w-full">
                      <span className="text-lg">{option}</span>
                      {showResult && index === currentQuestion.correctAnswer && (
                        <CheckCircle className="w-6 h-6 text-green-300" />
                      )}
                      {showResult && index === selectedAnswer && index !== currentQuestion.correctAnswer && (
                        <XCircle className="w-6 h-6 text-red-300" />
                      )}
                    </div>
                  </Button>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Next Button */}
        {showResult && (
          <div className="text-center">
            <Button
              onClick={handleNextQuestion}
              className={`bg-gradient-to-r ${getCategoryColor()} text-white px-8 py-3 text-lg font-semibold hover:shadow-xl transition-all duration-300`}
            >
              {currentQuestionIndex < questions.length - 1 ? "Next Question" : "See Results"}
            </Button>
          </div>
        )}

        {/* Score Display */}
        <div className="fixed bottom-6 right-6 bg-black/50 backdrop-blur-sm rounded-lg p-4 border border-gray-700">
          <p className="text-white font-semibold">
            Score: {score}/{questions.length}
          </p>
        </div>
      </div>
    </div>
  );
};

export default QuizPage;
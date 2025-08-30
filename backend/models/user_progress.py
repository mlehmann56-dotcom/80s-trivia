from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime
import uuid

class QuestionAnswer(BaseModel):
    questionId: str
    selectedAnswer: int
    correct: bool
    timeSpent: Optional[int] = None

class CategoryProgress(BaseModel):
    score: int = 0  # Percentage score
    completed: bool = False
    completedAt: Optional[datetime] = None
    attempts: int = 0
    bestScore: int = 0
    answers: List[QuestionAnswer] = []

class UserProgress(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sessionId: str
    levels: Dict[str, Dict[str, CategoryProgress]] = {}
    currentLevel: int = 1
    totalQuestionsAnswered: int = 0
    totalCorrectAnswers: int = 0
    averageScore: float = 0.0
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)

class ProgressUpdate(BaseModel):
    sessionId: str
    level: int
    category: str
    score: int
    totalQuestions: int
    completedAt: datetime = Field(default_factory=datetime.utcnow)
    answers: List[QuestionAnswer]

class LevelInfo(BaseModel):
    level: int
    name: str
    description: str
    requiredScore: int = 80
    unlocked: bool = False
    progress: Dict[str, CategoryProgress] = {}
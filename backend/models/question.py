from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class QuestionMetadata(BaseModel):
    explanation: Optional[str] = None
    tags: List[str] = []

class Question(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str
    options: List[str]  # Array of 4 options
    correctAnswer: int  # Index of correct option (0-3)
    difficulty: str  # easy, medium, hard, expert
    level: int  # 1-10
    category: str  # music, movies, fashion, general
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    metadata: QuestionMetadata = Field(default_factory=QuestionMetadata)

class QuestionCreate(BaseModel):
    question: str
    options: List[str]
    correctAnswer: int
    difficulty: str
    level: int
    category: str
    metadata: Optional[QuestionMetadata] = None

class QuestionResponse(BaseModel):
    questions: List[Question]
    count: int
    level: int
    category: str
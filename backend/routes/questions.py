from fastapi import APIRouter, HTTPException, Depends
from models.question import Question, QuestionCreate, QuestionResponse
from services.question_service import QuestionService
from typing import List, Optional
from database import get_question_service

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/{level}/{category}", response_model=QuestionResponse)
async def get_questions_by_level_category(
    level: int,
    category: str,
    limit: Optional[int] = None,
    question_service: QuestionService = Depends(get_question_service)
):
    """Get questions for specific level and category"""
    if level < 1 or level > 10:
        raise HTTPException(status_code=400, detail="Level must be between 1 and 10")
    
    if category not in ["music", "movies", "fashion", "general"]:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    try:
        questions = await question_service.get_questions_by_level_and_category(level, category, limit)
        
        return QuestionResponse(
            questions=questions,
            count=len(questions),
            level=level,
            category=category
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve questions: {str(e)}")

@router.get("/random/{level}/{category}/{count}")
async def get_random_questions(
    level: int,
    category: str, 
    count: int,
    question_service: QuestionService = Depends(get_question_service)
):
    """Get random subset of questions for quiz"""
    if level < 1 or level > 10:
        raise HTTPException(status_code=400, detail="Level must be between 1 and 10")
    
    if category not in ["music", "movies", "fashion", "general"]:
        raise HTTPException(status_code=400, detail="Invalid category")
        
    if count < 1 or count > 50:
        raise HTTPException(status_code=400, detail="Count must be between 1 and 50")
    
    try:
        questions = await question_service.get_random_questions(level, category, count)
        
        return QuestionResponse(
            questions=questions,
            count=len(questions),
            level=level,
            category=category
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve random questions: {str(e)}")

@router.get("/stats")
async def get_questions_stats(
    question_service: QuestionService = Depends(get_question_service)
):
    """Get question counts by level and category"""
    try:
        counts = await question_service.get_questions_count_by_level_category()
        return {"counts": counts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve question stats: {str(e)}")

@router.post("/", response_model=Question)
async def create_question(
    question_data: QuestionCreate,
    question_service: QuestionService = Depends(get_question_service)
):
    """Create a new question (admin endpoint)"""
    if len(question_data.options) != 4:
        raise HTTPException(status_code=400, detail="Question must have exactly 4 options")
    
    if question_data.correctAnswer < 0 or question_data.correctAnswer > 3:
        raise HTTPException(status_code=400, detail="Correct answer must be between 0 and 3")
    
    try:
        question = await question_service.create_question(question_data)
        return question
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create question: {str(e)}")
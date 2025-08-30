from fastapi import APIRouter, HTTPException, Depends
from models.user_progress import UserProgress, ProgressUpdate, LevelInfo
from services.user_progress_service import UserProgressService
from typing import List
from database import get_user_progress_service

router = APIRouter(prefix="/user", tags=["user_progress"]) 

@router.get("/progress/{session_id}", response_model=UserProgress)
async def get_user_progress(
    session_id: str,
    progress_service: UserProgressService = Depends(get_user_progress_service)
):
    """Get user's complete progress"""
    try:
        progress = await progress_service.get_or_create_user_progress(session_id)
        return progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user progress: {str(e)}")

@router.post("/progress", response_model=UserProgress)
async def update_user_progress(
    update_data: ProgressUpdate,
    progress_service: UserProgressService = Depends(get_user_progress_service)
):
    """Save user quiz results and update progress"""
    if update_data.level < 1 or update_data.level > 10:
        raise HTTPException(status_code=400, detail="Level must be between 1 and 10")
    
    if update_data.category not in ["music", "movies", "fashion", "general"]:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    if update_data.score < 0 or update_data.score > 100:
        raise HTTPException(status_code=400, detail="Score must be between 0 and 100")
    
    try:
        updated_progress = await progress_service.update_category_progress(update_data)
        return updated_progress
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user progress: {str(e)}")

@router.get("/levels/{session_id}", response_model=List[LevelInfo])
async def get_level_progress_summary(
    session_id: str,
    progress_service: UserProgressService = Depends(get_user_progress_service)
):
    """Get progress summary for all levels"""
    try:
        level_summaries = await progress_service.get_level_progress_summary(session_id)
        return level_summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve level progress: {str(e)}")

@router.get("/levels/{level}/unlock-status/{session_id}")
async def check_level_unlock_status(
    level: int,
    session_id: str,
    progress_service: UserProgressService = Depends(get_user_progress_service)
):
    """Check if level is unlocked for user"""
    if level < 1 or level > 10:
        raise HTTPException(status_code=400, detail="Level must be between 1 and 10")
    
    try:
        unlocked = await progress_service.is_level_unlocked(session_id, level)
        return {
            "level": level,
            "unlocked": unlocked,
            "sessionId": session_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check unlock status: {str(e)}")

@router.get("/leaderboard")
async def get_leaderboard(
    limit: int = 10,
    progress_service: UserProgressService = Depends(get_user_progress_service)
):
    """Get top performers leaderboard"""
    try:
        leaderboard = await progress_service.get_leaderboard(limit)
        return {"leaderboard": leaderboard, "count": len(leaderboard)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve leaderboard: {str(e)}")

@router.delete("/progress/{session_id}")
async def reset_user_progress(
    session_id: str,
    progress_service: UserProgressService = Depends(get_user_progress_service)
):
    """Reset user progress (for testing/admin purposes)"""
    try:
        await progress_service.collection.delete_one({"sessionId": session_id})
        return {"message": f"Progress reset for session {session_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset progress: {str(e)}")
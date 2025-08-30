from motor.motor_asyncio import AsyncIOMotorDatabase
from models.user_progress import UserProgress, ProgressUpdate, CategoryProgress, LevelInfo
from typing import Optional, Dict, List
from datetime import datetime

class UserProgressService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.user_progress

    async def get_or_create_user_progress(self, session_id: str) -> UserProgress:
        """Get existing user progress or create new one"""
        existing = await self.collection.find_one({"sessionId": session_id})
        
        if existing:
            return UserProgress(**existing)
        
        # Create new user progress
        new_progress = UserProgress(sessionId=session_id)
        await self.collection.insert_one(new_progress.dict())
        return new_progress

    async def update_category_progress(self, update_data: ProgressUpdate) -> UserProgress:
        """Update progress for a specific category"""
        user_progress = await self.get_or_create_user_progress(update_data.sessionId)
        
        # Initialize level if not exists
        level_key = str(update_data.level)
        if level_key not in user_progress.levels:
            user_progress.levels[level_key] = {}
        
        # Initialize category if not exists
        if update_data.category not in user_progress.levels[level_key]:
            user_progress.levels[level_key][update_data.category] = CategoryProgress()
        
        category_progress = user_progress.levels[level_key][update_data.category]
        
        # Update category progress
        category_progress.score = update_data.score
        category_progress.completed = True
        category_progress.completedAt = update_data.completedAt
        category_progress.attempts += 1
        category_progress.bestScore = max(category_progress.bestScore, update_data.score)
        category_progress.answers = update_data.answers
        
        # Update overall stats
        user_progress.totalQuestionsAnswered += update_data.totalQuestions
        correct_answers = len([a for a in update_data.answers if a.correct])
        user_progress.totalCorrectAnswers += correct_answers
        
        # Recalculate average score
        if user_progress.totalQuestionsAnswered > 0:
            user_progress.averageScore = (
                user_progress.totalCorrectAnswers / user_progress.totalQuestionsAnswered
            ) * 100
        
        user_progress.updatedAt = datetime.utcnow()
        
        # Save to database
        await self.collection.replace_one(
            {"sessionId": update_data.sessionId},
            user_progress.dict()
        )
        
        return user_progress

    async def is_level_unlocked(self, session_id: str, level: int) -> bool:
        """Check if a level is unlocked for the user"""
        if level == 1:
            return True
        
        user_progress = await self.get_or_create_user_progress(session_id)
        previous_level = str(level - 1)
        
        # Check if previous level exists and is completed
        if previous_level not in user_progress.levels:
            return False
        
        previous_level_data = user_progress.levels[previous_level]
        required_categories = ["music", "movies", "fashion", "general"]
        
        # Check if all categories in previous level are completed with 80%+
        for category in required_categories:
            if category not in previous_level_data:
                return False
            
            category_data = previous_level_data[category]
            if not category_data.completed or category_data.score < 80:
                return False
        
        return True

    async def get_level_progress_summary(self, session_id: str) -> List[LevelInfo]:
        """Get progress summary for all levels"""
        user_progress = await self.get_or_create_user_progress(session_id)
        
        level_summaries = []
        for level in range(1, 11):  # Levels 1-10
            level_data = user_progress.levels.get(str(level), {})
            
            level_info = LevelInfo(
                level=level,
                name=self.get_level_name(level),
                description=self.get_level_description(level),
                unlocked=await self.is_level_unlocked(session_id, level),
                progress=level_data
            )
            
            level_summaries.append(level_info)
        
        return level_summaries

    def get_level_name(self, level: int) -> str:
        """Get level name by number"""
        level_names = {
            1: "Rad Rookie",
            2: "New Wave Navigator", 
            3: "Synthpop Scholar",
            4: "Neon Master",
            5: "Retro Legend",
            6: "Time Machine Operator",
            7: "Totally Tubular Expert",
            8: "Awesome Archive",
            9: "Radical Repository",
            10: "Ultimate 80s Oracle"
        }
        return level_names.get(level, f"Level {level}")

    def get_level_description(self, level: int) -> str:
        """Get level description by number"""
        descriptions = {
            1: "Basic 80s knowledge",
            2: "Intermediate 80s trivia",
            3: "Advanced 80s expertise", 
            4: "Expert 80s knowledge",
            5: "Deep 80s specialist",
            6: "Comprehensive 80s guru",
            7: "Near-encyclopedic knowledge",
            8: "Professional-level expertise",
            9: "Academic-level mastery",
            10: "Supreme 80s wisdom"
        }
        return descriptions.get(level, f"Level {level} expertise")

    async def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top performers leaderboard"""
        pipeline = [
            {"$match": {"totalQuestionsAnswered": {"$gt": 0}}},
            {"$sort": {"averageScore": -1, "totalQuestionsAnswered": -1}},
            {"$limit": limit},
            {
                "$project": {
                    "sessionId": 1,
                    "averageScore": 1,
                    "totalQuestionsAnswered": 1,
                    "totalCorrectAnswers": 1,
                    "currentLevel": 1
                }
            }
        ]
        
        return await self.collection.aggregate(pipeline).to_list(None)
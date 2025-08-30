from motor.motor_asyncio import AsyncIOMotorDatabase
from models.question import Question, QuestionCreate
from typing import List, Optional
import random

class QuestionService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.questions

    async def create_question(self, question_data: QuestionCreate) -> Question:
        question = Question(**question_data.dict())
        await self.collection.insert_one(question.dict())
        return question

    async def get_questions_by_level_and_category(
        self, level: int, category: str, limit: Optional[int] = None
    ) -> List[Question]:
        query = {"level": level, "category": category}
        cursor = self.collection.find(query)
        
        if limit:
            cursor = cursor.limit(limit)
            
        questions_data = await cursor.to_list(None)
        return [Question(**q) for q in questions_data]

    async def get_random_questions(
        self, level: int, category: str, count: int
    ) -> List[Question]:
        # Get all questions for the level/category
        all_questions = await self.get_questions_by_level_and_category(level, category)
        
        # Return random subset
        if len(all_questions) <= count:
            return all_questions
        
        return random.sample(all_questions, count)

    async def get_question_by_id(self, question_id: str) -> Optional[Question]:
        question_data = await self.collection.find_one({"id": question_id})
        if question_data:
            return Question(**question_data)
        return None

    async def seed_questions(self, questions: List[QuestionCreate]):
        """Seed the database with initial questions"""
        # Clear existing questions first
        await self.collection.delete_many({})
        
        # Insert new questions
        question_docs = []
        for q_data in questions:
            question = Question(**q_data.dict())
            question_docs.append(question.dict())
        
        if question_docs:
            await self.collection.insert_many(question_docs)
        
        return len(question_docs)

    async def get_questions_count_by_level_category(self) -> dict:
        """Get count of questions by level and category"""
        pipeline = [
            {
                "$group": {
                    "_id": {"level": "$level", "category": "$category"},
                    "count": {"$sum": 1}
                }
            }
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(None)
        
        # Organize results by level and category
        counts = {}
        for item in result:
            level = str(item["_id"]["level"])
            category = item["_id"]["category"]
            
            if level not in counts:
                counts[level] = {}
            counts[level][category] = item["count"]
        
        return counts
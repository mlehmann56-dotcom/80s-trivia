from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from services.question_service import QuestionService
from services.user_progress_service import UserProgressService
import os

# Global database instance
client: AsyncIOMotorClient = None
database: AsyncIOMotorDatabase = None

def get_database() -> AsyncIOMotorDatabase:
    return database

def get_question_service() -> QuestionService:
    return QuestionService(database)

def get_user_progress_service() -> UserProgressService:
    return UserProgressService(database)

async def connect_to_mongo():
    """Create database connection"""
    global client, database
    
    mongo_url = os.environ['MONGO_URL']
    db_name = os.environ.get('DB_NAME', '80s_trivia')
    
    client = AsyncIOMotorClient(mongo_url)
    database = client[db_name]
    
    # Test the connection
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")
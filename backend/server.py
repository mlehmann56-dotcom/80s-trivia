from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
import os
import logging
from pathlib import Path
from database import connect_to_mongo, close_mongo_connection
from routes import questions, user_progress
from services.question_service import QuestionService
from seed_data import get_seed_questions

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Add your routes to the router
@api_router.get("/")
async def root():
    return {"message": "80s Trivia API - Let's get radical!"}

# Include route modules
api_router.include_router(questions.router)
api_router.include_router(user_progress.router)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection and seed data if needed"""
    await connect_to_mongo()
    logger.info("Connected to MongoDB")
    
    # Seed questions if database is empty
    from database import get_question_service
    question_service = get_question_service()
    
    # Check if questions already exist
    stats = await question_service.get_questions_count_by_level_category()
    if not stats:  # Database is empty
        logger.info("Seeding database with initial questions...")
        seed_questions = get_seed_questions()
        seeded_count = await question_service.seed_questions(seed_questions)
        logger.info(f"Seeded {seeded_count} questions into database")
    else:
        logger.info(f"Database already contains questions: {stats}")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection"""
    await close_mongo_connection()
    logger.info("Disconnected from MongoDB")

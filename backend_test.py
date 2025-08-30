#!/usr/bin/env python3
"""
Comprehensive Backend API Tests for 80s Trivia Game
Tests all major endpoints and functionality
"""

import asyncio
import aiohttp
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'https://neon-eighties.preview.emergentagent.com')
API_BASE = f"{BACKEND_URL}/api"

class TriviaTester:
    def __init__(self):
        self.session = None
        self.test_session_id = f"test_session_{uuid.uuid4().hex[:8]}"
        self.results = {
            "passed": 0,
            "failed": 0,
            "errors": []
        }
    
    async def setup(self):
        """Initialize HTTP session"""
        self.session = aiohttp.ClientSession()
    
    async def cleanup(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
    
    def log_result(self, test_name: str, success: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        
        if success:
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
            self.results["errors"].append(f"{test_name}: {message}")
    
    async def test_api_root(self):
        """Test API root endpoint"""
        try:
            async with self.session.get(f"{API_BASE}/") as response:
                if response.status == 200:
                    data = await response.json()
                    if "80s Trivia API" in data.get("message", ""):
                        self.log_result("API Root", True, "API is responding correctly")
                    else:
                        self.log_result("API Root", False, f"Unexpected message: {data}")
                else:
                    self.log_result("API Root", False, f"Status: {response.status}")
        except Exception as e:
            self.log_result("API Root", False, f"Exception: {str(e)}")
    
    async def test_questions_stats(self):
        """Test questions statistics endpoint"""
        try:
            async with self.session.get(f"{API_BASE}/questions/stats") as response:
                if response.status == 200:
                    data = await response.json()
                    counts = data.get("counts", {})
                    
                    # Check if we have level 1 data
                    if "1" in counts:
                        level_1 = counts["1"]
                        categories = ["music", "movies", "fashion", "general"]
                        all_categories_present = all(cat in level_1 for cat in categories)
                        
                        if all_categories_present:
                            total_questions = sum(level_1.values())
                            self.log_result("Questions Stats", True, 
                                          f"Found {total_questions} questions across all categories")
                        else:
                            missing = [cat for cat in categories if cat not in level_1]
                            self.log_result("Questions Stats", False, 
                                          f"Missing categories: {missing}")
                    else:
                        self.log_result("Questions Stats", False, "No level 1 questions found")
                else:
                    self.log_result("Questions Stats", False, f"Status: {response.status}")
        except Exception as e:
            self.log_result("Questions Stats", False, f"Exception: {str(e)}")
    
    async def test_get_questions_by_category(self):
        """Test getting questions for each category in level 1"""
        categories = ["music", "movies", "fashion", "general"]
        
        for category in categories:
            try:
                async with self.session.get(f"{API_BASE}/questions/1/{category}") as response:
                    if response.status == 200:
                        data = await response.json()
                        questions = data.get("questions", [])
                        
                        if len(questions) > 0:
                            # Verify question structure
                            first_question = questions[0]
                            required_fields = ["id", "question", "options", "correctAnswer", "level", "category"]
                            
                            if all(field in first_question for field in required_fields):
                                # Verify options array has 4 items
                                if len(first_question["options"]) == 4:
                                    # Verify correctAnswer is valid index
                                    if 0 <= first_question["correctAnswer"] <= 3:
                                        self.log_result(f"Questions - {category.title()}", True, 
                                                      f"Found {len(questions)} valid questions")
                                    else:
                                        self.log_result(f"Questions - {category.title()}", False, 
                                                      "Invalid correctAnswer index")
                                else:
                                    self.log_result(f"Questions - {category.title()}", False, 
                                                  f"Expected 4 options, got {len(first_question['options'])}")
                            else:
                                missing_fields = [f for f in required_fields if f not in first_question]
                                self.log_result(f"Questions - {category.title()}", False, 
                                              f"Missing fields: {missing_fields}")
                        else:
                            self.log_result(f"Questions - {category.title()}", False, "No questions found")
                    else:
                        self.log_result(f"Questions - {category.title()}", False, f"Status: {response.status}")
            except Exception as e:
                self.log_result(f"Questions - {category.title()}", False, f"Exception: {str(e)}")
    
    async def test_random_questions(self):
        """Test random questions endpoint"""
        try:
            async with self.session.get(f"{API_BASE}/questions/random/1/music/5") as response:
                if response.status == 200:
                    data = await response.json()
                    questions = data.get("questions", [])
                    
                    if len(questions) <= 5:  # Should be 5 or less if not enough questions
                        # Test that questions are properly formatted
                        if questions and all("id" in q for q in questions):
                            self.log_result("Random Questions", True, 
                                          f"Retrieved {len(questions)} random questions")
                        else:
                            self.log_result("Random Questions", False, "Invalid question format")
                    else:
                        self.log_result("Random Questions", False, f"Too many questions returned: {len(questions)}")
                else:
                    self.log_result("Random Questions", False, f"Status: {response.status}")
        except Exception as e:
            self.log_result("Random Questions", False, f"Exception: {str(e)}")
    
    async def test_invalid_parameters(self):
        """Test error handling for invalid parameters"""
        test_cases = [
            ("/questions/0/music", "Invalid level (too low)"),
            ("/questions/11/music", "Invalid level (too high)"),
            ("/questions/1/invalid", "Invalid category"),
            ("/questions/random/1/music/0", "Invalid count (too low)"),
            ("/questions/random/1/music/51", "Invalid count (too high)")
        ]
        
        for endpoint, description in test_cases:
            try:
                async with self.session.get(f"{API_BASE}{endpoint}") as response:
                    if response.status == 400:
                        self.log_result(f"Error Handling - {description}", True, "Correctly returned 400")
                    else:
                        self.log_result(f"Error Handling - {description}", False, 
                                      f"Expected 400, got {response.status}")
            except Exception as e:
                self.log_result(f"Error Handling - {description}", False, f"Exception: {str(e)}")
    
    async def test_user_progress_creation(self):
        """Test user progress creation and retrieval"""
        try:
            async with self.session.get(f"{API_BASE}/user/progress/{self.test_session_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Verify progress structure
                    required_fields = ["id", "sessionId", "levels", "currentLevel", "totalQuestionsAnswered"]
                    if all(field in data for field in required_fields):
                        if data["sessionId"] == self.test_session_id:
                            self.log_result("User Progress Creation", True, "Progress created successfully")
                            return data
                        else:
                            self.log_result("User Progress Creation", False, "Session ID mismatch")
                    else:
                        missing = [f for f in required_fields if f not in data]
                        self.log_result("User Progress Creation", False, f"Missing fields: {missing}")
                else:
                    self.log_result("User Progress Creation", False, f"Status: {response.status}")
        except Exception as e:
            self.log_result("User Progress Creation", False, f"Exception: {str(e)}")
        
        return None
    
    async def test_level_unlock_status(self):
        """Test level unlock status"""
        try:
            # Test level 1 (should be unlocked)
            async with self.session.get(f"{API_BASE}/user/levels/1/unlock-status/{self.test_session_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("unlocked") == True:
                        self.log_result("Level 1 Unlock Status", True, "Level 1 is unlocked")
                    else:
                        self.log_result("Level 1 Unlock Status", False, "Level 1 should be unlocked")
                else:
                    self.log_result("Level 1 Unlock Status", False, f"Status: {response.status}")
            
            # Test level 2 (should be locked initially)
            async with self.session.get(f"{API_BASE}/user/levels/2/unlock-status/{self.test_session_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("unlocked") == False:
                        self.log_result("Level 2 Unlock Status", True, "Level 2 is locked (correct)")
                    else:
                        self.log_result("Level 2 Unlock Status", False, "Level 2 should be locked initially")
                else:
                    self.log_result("Level 2 Unlock Status", False, f"Status: {response.status}")
        except Exception as e:
            self.log_result("Level Unlock Status", False, f"Exception: {str(e)}")
    
    async def test_progress_update(self):
        """Test updating user progress"""
        # Create sample quiz answers
        sample_answers = [
            {"questionId": f"q_{i}", "selectedAnswer": i % 4, "correct": i % 2 == 0, "timeSpent": 10}
            for i in range(5)
        ]
        
        progress_data = {
            "sessionId": self.test_session_id,
            "level": 1,
            "category": "music",
            "score": 80,
            "totalQuestions": 5,
            "completedAt": datetime.utcnow().isoformat(),
            "answers": sample_answers
        }
        
        try:
            async with self.session.post(f"{API_BASE}/user/progress", 
                                       json=progress_data,
                                       headers={"Content-Type": "application/json"}) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # Verify the progress was updated
                    if "levels" in data and "1" in data["levels"]:
                        level_1 = data["levels"]["1"]
                        if "music" in level_1:
                            music_progress = level_1["music"]
                            if music_progress.get("score") == 80 and music_progress.get("completed") == True:
                                self.log_result("Progress Update", True, "Progress updated successfully")
                            else:
                                self.log_result("Progress Update", False, "Progress data incorrect")
                        else:
                            self.log_result("Progress Update", False, "Music category not found")
                    else:
                        self.log_result("Progress Update", False, "Level 1 data not found")
                else:
                    response_text = await response.text()
                    self.log_result("Progress Update", False, f"Status: {response.status}, Response: {response_text}")
        except Exception as e:
            self.log_result("Progress Update", False, f"Exception: {str(e)}")
    
    async def test_level_progress_summary(self):
        """Test level progress summary"""
        try:
            async with self.session.get(f"{API_BASE}/user/levels/{self.test_session_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if isinstance(data, list) and len(data) == 10:  # Should have 10 levels
                        first_level = data[0]
                        required_fields = ["level", "name", "description", "unlocked"]
                        
                        if all(field in first_level for field in required_fields):
                            # Check that level 1 is unlocked
                            if first_level["unlocked"] == True:
                                self.log_result("Level Progress Summary", True, 
                                              f"Retrieved summary for {len(data)} levels")
                            else:
                                self.log_result("Level Progress Summary", False, "Level 1 should be unlocked")
                        else:
                            missing = [f for f in required_fields if f not in first_level]
                            self.log_result("Level Progress Summary", False, f"Missing fields: {missing}")
                    else:
                        self.log_result("Level Progress Summary", False, 
                                      f"Expected 10 levels, got {len(data) if isinstance(data, list) else 'non-list'}")
                else:
                    self.log_result("Level Progress Summary", False, f"Status: {response.status}")
        except Exception as e:
            self.log_result("Level Progress Summary", False, f"Exception: {str(e)}")
    
    async def test_leaderboard(self):
        """Test leaderboard endpoint"""
        try:
            async with self.session.get(f"{API_BASE}/user/leaderboard") as response:
                if response.status == 200:
                    data = await response.json()
                    
                    if "leaderboard" in data and "count" in data:
                        leaderboard = data["leaderboard"]
                        if isinstance(leaderboard, list):
                            self.log_result("Leaderboard", True, 
                                          f"Retrieved leaderboard with {len(leaderboard)} entries")
                        else:
                            self.log_result("Leaderboard", False, "Leaderboard is not a list")
                    else:
                        self.log_result("Leaderboard", False, "Missing leaderboard or count fields")
                else:
                    self.log_result("Leaderboard", False, f"Status: {response.status}")
        except Exception as e:
            self.log_result("Leaderboard", False, f"Exception: {str(e)}")
    
    async def test_full_quiz_flow(self):
        """Test complete quiz flow: get questions -> answer -> save progress"""
        try:
            # Step 1: Get questions for fashion category
            async with self.session.get(f"{API_BASE}/questions/random/1/fashion/3") as response:
                if response.status != 200:
                    self.log_result("Full Quiz Flow", False, "Failed to get questions")
                    return
                
                questions_data = await response.json()
                questions = questions_data.get("questions", [])
                
                if len(questions) == 0:
                    self.log_result("Full Quiz Flow", False, "No questions retrieved")
                    return
            
            # Step 2: Simulate answering questions
            answers = []
            correct_count = 0
            for i, question in enumerate(questions):
                # Simulate correct answer for first question, wrong for others
                selected_answer = question["correctAnswer"] if i == 0 else (question["correctAnswer"] + 1) % 4
                is_correct = selected_answer == question["correctAnswer"]
                if is_correct:
                    correct_count += 1
                
                answers.append({
                    "questionId": question["id"],
                    "selectedAnswer": selected_answer,
                    "correct": is_correct,
                    "timeSpent": 15
                })
            
            # Step 3: Calculate score and save progress
            score = int((correct_count / len(questions)) * 100)
            
            progress_data = {
                "sessionId": self.test_session_id,
                "level": 1,
                "category": "fashion",
                "score": score,
                "totalQuestions": len(questions),
                "completedAt": datetime.utcnow().isoformat(),
                "answers": answers
            }
            
            async with self.session.post(f"{API_BASE}/user/progress", 
                                       json=progress_data,
                                       headers={"Content-Type": "application/json"}) as response:
                if response.status == 200:
                    # Step 4: Verify progress was saved
                    async with self.session.get(f"{API_BASE}/user/progress/{self.test_session_id}") as verify_response:
                        if verify_response.status == 200:
                            progress = await verify_response.json()
                            if ("1" in progress.get("levels", {}) and 
                                "fashion" in progress["levels"]["1"] and
                                progress["levels"]["1"]["fashion"]["completed"]):
                                self.log_result("Full Quiz Flow", True, 
                                              f"Complete flow successful (score: {score}%)")
                            else:
                                self.log_result("Full Quiz Flow", False, "Progress not properly saved")
                        else:
                            self.log_result("Full Quiz Flow", False, "Failed to verify progress")
                else:
                    self.log_result("Full Quiz Flow", False, "Failed to save progress")
        
        except Exception as e:
            self.log_result("Full Quiz Flow", False, f"Exception: {str(e)}")
    
    async def test_data_persistence(self):
        """Test that data persists across API calls"""
        try:
            # Get initial progress
            async with self.session.get(f"{API_BASE}/user/progress/{self.test_session_id}") as response:
                if response.status != 200:
                    self.log_result("Data Persistence", False, "Failed to get initial progress")
                    return
                
                initial_progress = await response.json()
                initial_total = initial_progress.get("totalQuestionsAnswered", 0)
            
            # Add more progress
            sample_answers = [
                {"questionId": f"persist_q_{i}", "selectedAnswer": 0, "correct": True, "timeSpent": 12}
                for i in range(3)
            ]
            
            progress_data = {
                "sessionId": self.test_session_id,
                "level": 1,
                "category": "general",
                "score": 100,
                "totalQuestions": 3,
                "completedAt": datetime.utcnow().isoformat(),
                "answers": sample_answers
            }
            
            async with self.session.post(f"{API_BASE}/user/progress", 
                                       json=progress_data,
                                       headers={"Content-Type": "application/json"}) as response:
                if response.status != 200:
                    self.log_result("Data Persistence", False, "Failed to update progress")
                    return
            
            # Verify persistence
            async with self.session.get(f"{API_BASE}/user/progress/{self.test_session_id}") as response:
                if response.status == 200:
                    final_progress = await response.json()
                    final_total = final_progress.get("totalQuestionsAnswered", 0)
                    
                    if final_total == initial_total + 3:
                        self.log_result("Data Persistence", True, 
                                      f"Data persisted correctly ({initial_total} -> {final_total})")
                    else:
                        self.log_result("Data Persistence", False, 
                                      f"Data not persisted correctly ({initial_total} -> {final_total})")
                else:
                    self.log_result("Data Persistence", False, "Failed to verify final progress")
        
        except Exception as e:
            self.log_result("Data Persistence", False, f"Exception: {str(e)}")
    
    async def cleanup_test_data(self):
        """Clean up test data"""
        try:
            async with self.session.delete(f"{API_BASE}/user/progress/{self.test_session_id}") as response:
                if response.status == 200:
                    print(f"✅ Cleaned up test data for session: {self.test_session_id}")
                else:
                    print(f"⚠️  Failed to clean up test data: {response.status}")
        except Exception as e:
            print(f"⚠️  Error during cleanup: {str(e)}")
    
    async def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting 80s Trivia Backend API Tests")
        print(f"📡 Testing API at: {API_BASE}")
        print(f"🔑 Test Session ID: {self.test_session_id}")
        print("=" * 60)
        
        await self.setup()
        
        try:
            # Core API tests
            await self.test_api_root()
            await self.test_questions_stats()
            await self.test_get_questions_by_category()
            await self.test_random_questions()
            await self.test_invalid_parameters()
            
            # User progress tests
            await self.test_user_progress_creation()
            await self.test_level_unlock_status()
            await self.test_progress_update()
            await self.test_level_progress_summary()
            await self.test_leaderboard()
            
            # Integration tests
            await self.test_full_quiz_flow()
            await self.test_data_persistence()
            
            # Cleanup
            await self.cleanup_test_data()
            
        finally:
            await self.cleanup()
        
        # Print summary
        print("=" * 60)
        print("📊 TEST SUMMARY")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        
        if self.results['errors']:
            print("\n🔍 FAILED TESTS:")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        success_rate = (self.results['passed'] / (self.results['passed'] + self.results['failed'])) * 100
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        if self.results['failed'] == 0:
            print("🎉 All tests passed! Backend is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the errors above.")
        
        return self.results['failed'] == 0

async def main():
    """Main test runner"""
    tester = TriviaTester()
    success = await tester.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
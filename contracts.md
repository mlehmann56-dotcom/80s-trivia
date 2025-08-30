# 80s Trivia App - Backend Integration Contracts

## Current Mock Data to Replace

### 1. Questions Data
- **Current**: `mockQuestionsLevels.js` with static question objects
- **Backend Replacement**: MongoDB collection with dynamic question retrieval
- **Structure**: Questions organized by level (1-10) and category (music, movies, fashion, general)

### 2. User Progress Data
- **Current**: localStorage with user progress tracking
- **Backend Replacement**: User sessions and progress stored in database
- **Structure**: User progress by level/category with scores and completion status

### 3. Level Information
- **Current**: Static `levelInfo` object with level names/descriptions
- **Backend Replacement**: Can remain static or move to database for easy updates

## API Contracts to Implement

### Questions Endpoints

#### GET /api/questions/:level/:category
- **Purpose**: Retrieve questions for specific level and category
- **Parameters**: 
  - `level`: 1-10
  - `category`: music, movies, fashion, general
- **Response**: Array of question objects
```json
{
  "questions": [
    {
      "id": "string",
      "question": "string",
      "options": ["string", "string", "string", "string"],
      "correctAnswer": number,
      "difficulty": "easy|medium|hard|expert",
      "level": number,
      "category": "string"
    }
  ]
}
```

#### GET /api/questions/random/:level/:category/:count
- **Purpose**: Get random subset of questions for quiz
- **Parameters**: level, category, count (number of questions)
- **Response**: Random question array

### User Progress Endpoints

#### POST /api/user/progress
- **Purpose**: Save user quiz results
- **Body**:
```json
{
  "sessionId": "string",
  "level": number,
  "category": "string",
  "score": number,
  "totalQuestions": number,
  "completedAt": "ISO date string",
  "answers": [
    {
      "questionId": "string",
      "selectedAnswer": number,
      "correct": boolean,
      "timeSpent": number
    }
  ]
}
```
- **Response**: Updated user progress object

#### GET /api/user/progress/:sessionId
- **Purpose**: Retrieve user's complete progress
- **Response**: User progress across all levels/categories
```json
{
  "sessionId": "string",
  "levels": {
    "1": {
      "music": {
        "score": number,
        "completed": boolean,
        "completedAt": "ISO date"
      }
    }
  },
  "currentLevel": number,
  "totalQuestionsAnswered": number,
  "averageScore": number
}
```

#### GET /api/user/leaderboard
- **Purpose**: Get top performers (optional feature)
- **Response**: Array of top scores by level

### Level Information Endpoints

#### GET /api/levels
- **Purpose**: Get all level information
- **Response**: Level metadata (names, descriptions, requirements)

#### GET /api/levels/:level/unlock-status/:sessionId
- **Purpose**: Check if level is unlocked for user
- **Response**: Boolean unlock status and requirements

## Database Schema Design

### Questions Collection
```javascript
{
  _id: ObjectId,
  id: String, // Unique question identifier
  question: String,
  options: [String], // Array of 4 options
  correctAnswer: Number, // Index of correct option (0-3)
  difficulty: String, // easy, medium, hard, expert  
  level: Number, // 1-10
  category: String, // music, movies, fashion, general
  createdAt: Date,
  metadata: {
    explanation: String, // Optional explanation for answer
    tags: [String], // Optional tags for question categorization
  }
}
```

### User Progress Collection
```javascript
{
  _id: ObjectId,
  sessionId: String, // Unique session identifier
  levels: {
    "1": {
      "music": {
        score: Number, // Percentage score
        completed: Boolean,
        completedAt: Date,
        attempts: Number,
        bestScore: Number,
        answers: [
          {
            questionId: String,
            selectedAnswer: Number,
            correct: Boolean,
            timeSpent: Number
          }
        ]
      }
      // ... other categories
    }
    // ... other levels
  },
  currentLevel: Number,
  totalQuestionsAnswered: Number,
  totalCorrectAnswers: Number,
  averageScore: Number,
  createdAt: Date,
  updatedAt: Date
}
```

### Level Information Collection (Optional)
```javascript
{
  _id: ObjectId,
  level: Number,
  name: String,
  description: String,
  requiredScore: Number, // 80
  unlockRequirements: {
    previousLevelCompletion: Boolean,
    minimumCategoriesRequired: Number // 4
  }
}
```

## Frontend Integration Changes

### 1. Replace Mock Data Usage
- Remove imports from `mockQuestionsLevels.js`
- Replace with API calls to fetch questions dynamically
- Update `levelProgressionUtils.js` to work with API data

### 2. Session Management
- Generate unique session ID on app start
- Store session ID in localStorage
- Pass session ID with all API requests

### 3. API Integration Points
- **HomePage/LevelSelector**: Call `/api/user/progress/:sessionId` to load progress
- **CategorySelector**: Call `/api/levels/:level/unlock-status/:sessionId` for unlock checks
- **QuizPage**: Call `/api/questions/:level/:category` to load questions
- **ResultsPage**: Call `/api/user/progress` to save results

### 4. Loading States
- Add loading spinners for API calls
- Handle error states gracefully
- Cache frequently accessed data

## Business Logic Implementation

### 1. Level Unlock Logic
- User must complete ALL 4 categories in current level with 80%+ score
- Only then next level becomes available
- Backend validates unlock status on each request

### 2. Score Calculation
- Percentage score = (correct answers / total questions) * 100
- Track best score per category/level
- Update user's overall average score

### 3. Question Selection
- Random selection from available questions in level/category
- Avoid duplicate questions in same session (optional)
- Support for question difficulty progression

## Migration Strategy

### Phase 1: Backend Setup
1. Create MongoDB models and seed initial question data
2. Implement question retrieval endpoints
3. Test question fetching with existing frontend

### Phase 2: User Progress Integration  
1. Implement user progress endpoints
2. Update frontend to use session-based progress
3. Migrate localStorage data handling to API calls

### Phase 3: Enhanced Features
1. Add leaderboard functionality
2. Implement question analytics
3. Add admin endpoints for question management

## Error Handling

### API Error Responses
```json
{
  "error": true,
  "message": "string",
  "code": "ERROR_CODE",
  "details": {} // Optional additional error details
}
```

### Frontend Error Handling
- Graceful fallback to cached data when API fails
- User-friendly error messages
- Retry mechanisms for failed requests
- Offline mode support (using localStorage as backup)

## Testing Strategy

### Backend Testing
- Unit tests for all API endpoints
- Integration tests for database operations
- Load testing for question retrieval performance

### Frontend Integration Testing
- Test API integration points
- Verify progress synchronization
- Test offline/online mode switching
- Validate level unlock logic end-to-end
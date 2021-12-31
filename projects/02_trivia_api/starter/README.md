# Full Stack API Final Project


## Introduction

Trivia application is a quiz game that helps bonding experiences for its employees and students.

What you can do in application:

1. See a list of questions: both all questions and by category.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Instructions for how to install project dependencies and start the project server

### 1. Backend Dependencies

The tech stack includes the following:

* `Anaconda` as a tool to create isolated Python environments.
* `SQLAlchemy` ORM to be the ORM library of choice.
* `Flask-Cors` as a Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible
* `PostgreSQL` as the database of choice.
* `Python3` and `Flask` as the server language and server framework.

### 2. Frontend Dependencies

You must have the **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```

### 3. Setup and launch

1. Clone project from [GitHub repository](https://github.com/artiomdiu/trivia/tree/master).

2. Download and install backend dependencies using pip:
```
pip install -r ./backend/requirements.txt
```

4. Run the backend server from /backend folder:
```
export FLASK_APP=__init__
export FLASK_ENV=development
python __init__.py
```

5. Verify on browser that development server is up by navigating to http://127.0.0.1:5000/

6. Install frontend packages and launch frontend server from ./frontend folder:
```
npm install // only once to install dependencies
npm start
```

7. Verify on browser that development server is up by navigating to http://127.0.0.1:3000

8. Launch unit tests from ./backend folder:
```
python test_flaskr.py
```

## API reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable

### Endpoints

#### GET /categories
- General:
    - Returns a list of categories.
- Sample: `curl http://127.0.0.1:5000/categories`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

#### GET /questions
- General:
    - Returns a list of questions, number of total questions, categories and a success value.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions?page=1`
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "success": true,
  "totalQuestions": 18
}
```

#### DELETE /questions/{id}
- General:
    - Deletes the question of the given ID if it exists. Returns a success value.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1`
```
{
  "success": true
}
```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, difficulty and chosen category. Returns a success value. 
- Sample:`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"test question", "answer":"test answer", "difficulty":"4", "category":"2"}'`
```
{
  "success": true
}
```
- General:
    - Returns a list of found questions based on search term, total number of questions and a success value. 
- Sample:`curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"soccer"}'`
```
{
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "totalQuestions": 18
}
```

#### GET /categories/{id}/questions
- General:
    - Returns a list of questions for a given category, number of total questions and a success value.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/categories/2/questions?page=1`
```
{
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    },
    {
      "answer": "test answer",
      "category": 2,
      "difficulty": 4,
      "id": 25,
      "question": "test question"
    }
  ],
  "success": true,
  "totalQuestions": 5
}
```

#### POST /quizzes
- General:
    - This endpoint takes category and previous question parameters and returns a random questions within the given category, if provided, and that is not one of the previous questions. Returns question and a success value. 
- Sample:`curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[16, 17], "quiz_category":{"type": "Art", "id":"2"}}'`
```
{
  "question": {
    "answer": "test answer",
    "category": 2,
    "difficulty": 4,
    "id": 25,
    "question": "test question"
  },
  "success": true
}
```
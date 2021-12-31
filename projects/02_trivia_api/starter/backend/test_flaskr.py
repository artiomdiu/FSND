import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres',
            'postgres586',
            'localhost:5432',
            self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "Who won biggest amount of gold medals in Olympics?",
            "answer": "Michael Phelps",
            "difficulty": 3,
            "category": 6
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # @DONE
    # Write at least one test for each test
    # for successful operation and for expected errors.

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["categories"]), 6)

    def test_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"], True)
        self.assertGreater(data["totalQuestions"], 0)
        self.assertTrue(data["categories"], True)

    def test_404_send_invalid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    # def test_delete_question(self):
    #     res = self.client().delete("/questions/2")
    #     data = json.loads(res.data)
    #
    #     question = Question.query.filter(Question.id == 2).one_or_none()
    #
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(question, None)
    #
    # def test_delete_invalid_question(self):
    #     res = self.client().delete("/questions/1000")
    #     data = json.loads(res.data)
    #
    #     self.assertEqual(res.status_code, 422)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], "unprocessable")

    def test_post_new_question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)
        pass

    def test_get_question_search_with_results(self):
        res = self.client().post("/questions", json={"searchTerm": "soccer"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertEqual(len(data["questions"]), 2)

    def test_get_question_search_without_results(self):
        res = self.client().post("/questions", json={"searchTerm": "texttext"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["totalQuestions"])
        self.assertEqual(len(data["questions"]), 0)

    def test_get_questions_from_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])

    def test_get_next_question(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [20],
            "quiz_category": {'type': 'Science', 'id': '1'}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

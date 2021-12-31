import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def get_category_list():
    categories = {}
    for category in Category.query.order_by(Category.id).all():
        categories[category.id] = category.type
    return categories


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    # after_request decorator to set Access-Control-Allow

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE"
        )
        return response

    # Endpoint to handle GET requests for all available categories.

    @app.route("/categories", methods=["GET"])
    def retrieve_categories():
        try:
            categories = get_category_list()

            return {"categories": categories}
        except:
            abort(404)

    '''
    Endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint returns a list of questions,
    number of total questions, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route("/questions", methods=["GET"])
    def retrieve_questions():
        try:
            all_questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, all_questions)

            if len(current_questions) == 0:
                abort(404)

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "totalQuestions": len(all_questions),
                    "categories": get_category_list()
                }
            )
        except:
            abort(404)

    '''
    Endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    "success": True,
                }
            )
        except:
            abort(422)

    '''
    Endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    Moreover, endpoint to GET questions based on a search term.
    It returns any questions for whom the search term
    is a substring of the question.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route("/questions", methods=["POST"])
    def create_new_question():
        body = request.get_json()

        search = body.get("searchTerm", None)
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        try:
            if search:
                search_res = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search))
                )
                current_questions = paginate_questions(request, search_res)
                all_questions = Question.query.order_by(Question.id).all()

                return jsonify(
                    {
                        "success": True,
                        "questions": current_questions,
                        "totalQuestions": len(all_questions),
                    }
                )
            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category
                )
                question.insert()

                return jsonify(
                    {
                        "success": True
                    }
                )
        except:
            abort(422)

    '''
    Endpoint to GET questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route("/categories/<int:id>/questions", methods=["GET"])
    def get_questions_from_category(id):
        try:
            questions_in_cat = Question.query.order_by(Question.id).filter(
                Question.category == id
            ).all()
            current_questions = paginate_questions(request, questions_in_cat)

            if len(current_questions) == 0:
                abort(404)

            return {
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(questions_in_cat)
            }
        except:
            abort(404)

    '''
    POST endpoint to get questions to play the quiz.
    This endpoint takes category and previous question parameters
    and returns a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route("/quizzes", methods=["POST"])
    def get_quiz_questions():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)
        quiz_questions = []
        print(body)

        try:
            category_id = int(quiz_category["id"])

            if category_id == 0:
                category_questions = Question.query.all()
            else:
                category_questions = Question.query.filter(
                    Question.category == category_id).all()

            for question in category_questions:

                if question.id not in previous_questions:
                    quiz_questions.append(question.format())

            if len(quiz_questions) != 0:
                next_question = random.choice(quiz_questions)

                return jsonify(
                    {
                        "success": True,
                        "question": next_question
                    }
                )
            else:
                return jsonify(
                    {
                        "success": True,
                        "question": False
                    }
                )
        except:
            abort(422)

    '''
    Error handlers for all expected errors including 404 and 422.
    '''

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                }
            ),
            404
        )

    @app.errorhandler(422)
    def not_found(error):
        return (
            jsonify(
                {
                    "success": False,
                    "error": 422,
                    "message": "unprocessable"
                }
            ),
            422
        )

    return app

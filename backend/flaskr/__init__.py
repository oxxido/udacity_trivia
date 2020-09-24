import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_cors import CORS
import random

from models import setup_db, Question, Category
from dotenv import load_dotenv
load_dotenv()

QUESTIONS_PER_PAGE = int(os.getenv('QUESTIONS_PER_PAGE'))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
        ] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config[
        "SQLALCHEMY_TRACK_MODIFICATIONS"
        ] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

    setup_db(app)
    # pylint: disable=unused-variable
    # CORS Headers

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS'
        )
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    """
    get_formatted_categories

    Returns:
            Array: formatted categories
    """

    def get_formatted_categories():
        categories = Category.query.order_by(Category.id.asc()).all()
        if categories is None:
            return None
        else:
            format_categories = {
                category.id: category.type for category in categories
            }
            return format_categories

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def get_categories():
        categories = get_formatted_categories()
        if categories is None:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories,
            'count': len(categories)
        })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three
    pages. Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():

        current_page = int(request.args.get('page', 1))
        questions = Question.query.paginate(
            current_page,
            QUESTIONS_PER_PAGE,
            False
        )
        if questions is None:
            abort(404)
        format_questions = [qt.format() for qt in questions.items]
        format_categories = get_formatted_categories()
        return jsonify({
            'success': True,
            'questions': format_questions,
            'current_page': current_page,
            'total_questions': questions.total,
            'categories': format_categories,
        })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last
    page of the questions list in the "List" tab.
    '''

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = body.get('searchTerm', '')

        questions = Question.query.filter(
            Question.question.ilike(
                "%{0}%".format(search)
            )
        ).all()
        format_questions = [qt.format() for qt in questions]

        return jsonify({
            'success': True,
            "total_questions": len(format_questions),
            "questions": format_questions,
            "current_category": 0
        })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):

        questions = Question.query.filter(
            Question.category == category_id
            ).all()
        if questions is None:
            abort(404)
        format_questions = [qt.format() for qt in questions]
        return jsonify({
            'success': True,
            'questions': format_questions,
            'total_questions': len(format_questions),
            'categories': get_formatted_categories(),
            'current_category': category_id
        })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():

        # Get category and prev questions
        body = request.get_json()
        category = body.get('quiz_category', None).get('id')
        previous_questions = body.get('previous_questions', None)

        # Both vars are requied, so if not provided return error
        if category is None or previous_questions is None:
            abort(400)
        Q = Question.query

        # if provided with category, added to the filter
        if int(category) > 0:
            Q = Question.query.filter(Question.category == category)

        # Return first random question NOT IN previous questions
        question = Q.filter(
                ~Question.id.in_(previous_questions)
            ).order_by(func.random()).first()

        if question:
            question = question.format()
        return jsonify({
                'success': True,
                'question': question
            })

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.

    '''

    @app.errorhandler(400)
    def err_malformed(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Malformed request"
        }), 400

    @app.errorhandler(404)
    def err_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def err_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        }), 405

    return app

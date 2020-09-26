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

    def get_formatted_categories():
        """ Formatted Categories.
        get:
            summary: Return formatted categories.
            description: function to return an array of categories objects
            return:
                array: formatted categories
        """
        categories = Category.query.order_by(Category.id.asc()).all()
        if categories is None:
            return None
        else:
            format_categories = {
                category.id: category.type for category in categories
            }
            return format_categories


    @app.route('/categories', methods=['GET'])
    def get_categories():
        """ Categories route.
        get:
            summary: Category endpoint.
            description: Get current categories

            responses:
                200:
                    success: True
                    categories: Categories Array
                    count: amount of categories
                404:
                    description: if no categories on db.
        """
        categories = get_formatted_categories()
        if categories is None:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories,
            'count': len(categories)
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        """ Questions route.
        GET:
            summary: return array with questions
            description: Get paginated questions. If a search string is
                provided, it will return the seach result.
            parameters:
                - Page: int 
                    type: GET arg: ie '?page=1'
                    Desc: Page Number
            responses:
                200:
                    success: True,
                    questions: array of formatted questions,
                    current_page: (int) current page,
                    total_questions: (int) total questions in db,
                    categories: format_categories,
                404:
                    success: False,
                    message: error message.
                    code: 404
        """
        current_page = int(request.args.get('page', 1))
        search = request.args.get('question', None)
        q = Question.query
        # if it's a search, let's add it to the ORM as filter
        if search:
            q = q.filter(
                Question.question.ilike(
                    "%{0}%".format(search)
                )
            )
        # Using paginate built-in SQLAlquemy methods
        questions = q.paginate(
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

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_book(question_id):
        """ Question Delete Route.
        DELETE:
            summary: Deletes a question.
            description: Seaches for a question based on an id
                If found, it deletes the question.
            parameters:
                - question_id: int 
                    type: path parameter, ie: '/questions/4'
                    Desc: question db id
            responses:
                200:
                    success: True,
                    deleted: int with deleted question id
                422:
                    success: False,
                    message: error message.
                    code: 422
        """
        try:
            question = Question.query.filter(
                Question.id == question_id
            ).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id,
            })

        except Exception:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        """ add question Route.
        POST:
            summary: Inserts a new question on db.
            description: Takes vars from a form POST and insert
                the new question in db.
            parameters:
                - question: text
                - answer: text
                - difficulty: int, 1 to 5
                - category: int, category id.
            responses:
                200:
                    success: True,
                    created: int, question id
                    question: question object
                422:
                    success: False,
                    message: error message.
                    code: 422
        """
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            if new_question and new_answer:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    difficulty=new_difficulty,
                    category=new_category
                )
                question.insert()

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'question': question.format()
                })
            else:
                raise Exception("Parameters are Empty")
        except Exception:
            abort(422)

    @app.route('/categories/<int:category_id>/questions')
    def get_category_questions(category_id):
        """ Cagetories/$/questions route.
        GET:
            summary: Questions by category.
            description: Return a list of questions
                depending on the category
            parameters:
                - cateogory id: int 
                    type: path parameter, ie: '/categories/4/questions'
                    Desc: category db id
            responses:
                200:
                    success: True,
                    questions: array of question objects
                    total_questions: (int) total questions
                    categories: array of categories,
                    current_category: (int) current category
                404:
                    description: if no questions on db.
        """
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

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        """ quizzes route.
        POST:
            summary: Return a one question.
            description: This endpoint returns a question
                that belongs to a category, if category is provided
                and that is not one of the previous questions, according
                to a previous_question parameter.
            parameters:
                - quiz_category id: int 
                    type: POST parameter
                    Desc: category db id
                    required: yes, but it can be empty
                - previous_questions: arr
                    type: POST parameter
                    Desc: array of int: question ids
                    required: yes, but it can be empty
            responses:
                200:
                    success: True,
                    question: question object
                404:
                    description: if no questions on db.
        """
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

        # If question is an object, format it, otherwise var is None
        # which is the right functionality
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
    
    @app.errorhandler(422)
    def err_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    return app

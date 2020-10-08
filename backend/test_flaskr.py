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
        setup_db(self.app)

        self.new_question = {
            'question': 'What color is gree?',
            'answer': 'green',
            'difficulty': 3,
            'category': 1
        }

        self.empty_question = {
            'question': False,
            'answer': False,
            'difficulty': 3,
            'category': 1
        }
        self.quiz = {
            'quiz_category': {'id': 2},
            'previous_questions': [],
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

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    def test_post_categories(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_page'], 1)
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)
        self.assertEqual(len(data['categories']), 6)

    def test_page_out_of_bounds(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_search_with_results(self):
        res = self.client().get('/questions?question=to')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_page'], 1)
        self.assertEqual(len(data['categories']), 6)
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)

    def test_search_with_results_page_2(self):
        res = self.client().get('/questions?question=a&page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_page'], 2)
        self.assertEqual(len(data['categories']), 6)
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)

    def test_search_with_results_out_of_bounds(self):
        res = self.client().get('/questions?question=a&page=20')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_search_with_no_results(self):
        res = self.client().get('/questions?question=jacaranda')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_search_with_no_results_and_out_of_bounds(self):
        res = self.client().get('/questions?question=jacaranda&page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'] > 0)

    def test_create_new_empty_question_fails(self):
        res = self.client().post('/questions', json=self.empty_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_delete_question(self):
        # to be allow to succesfully delete a book on each test we need
        # to take the last question we created and delete it
        last_question = Question.query.order_by(Question.id.desc()).first()
        last_id = str(last_question.id)

        if last_question:
            res = self.client().delete('/questions/'+last_id)
            data = json.loads(res.data)

            question = Question.query.filter(
                Question.id == last_id
                ).one_or_none()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(str(data['deleted']), last_id)
            self.assertEqual(question, None)
        else:
            self.assertFalse("No last question id")

    def test_delete_unexisting_question(self):
        # to be allow to succesfully delete a book on each test we need
        # to take the last question we created and delete it
        res = self.client().delete('/questions/99999')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])

    def test_get_category_questions(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'] > 0)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['current_category'], 2)

    def test_start_quiz(self):
        res = self.client().post('/quizzes', json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])
        self.assertEqual(data['question']['category'], 2)

    def test_check_returned_ids_not_in_previous(self):

        # with test db, cat 2 must be at least 3 questions long
        question = Question.query.filter(
            Question.category == 2
            ).order_by(Question.id).first()
        question = question.format()
        question_id = question['id']
        self.quiz['previous_questions'] = [question_id]
        res = self.client().post('/quizzes', json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertNotEqual(data['question']['id'], question_id)

    def test_play_trivia(self):

        infinite_breaker = 0
        quiz = self.quiz
        # while we have questions, keep playing trivia
        # Added infinity breaker to avoid infinite loop
        while True:
            res = self.client().post('/quizzes', json=quiz)
            data = json.loads(res.data)
            if data['question'] is None:
                break

            # for each trivia call, check response
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['success'])
            self.assertTrue(data['question'])
            self.assertEqual(data['question']['category'], 2)

            # then add the question id to previous questions to avoid
            # getting repeated questions
            quiz['previous_questions'].append(data['question']['id'])
            infinite_breaker += 1
            if infinite_breaker > 20:
                self.assertFalse('Loop ran more than 20 times')
                break

    def test_get_unexisting_category_questions(self):
        res = self.client().get('/categories/99/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_malformed_quiz_request(self):
        self.quiz['quiz_category']['id'] = None
        res = self.client().post('/quizzes', json=self.quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_no_request_quiz_post(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])

    def test_json_404_return(self):
        res = self.client().get('/non_existing_page')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

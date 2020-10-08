# Udacity Trivia API Backend

Welcome to our Trivia API documentation. Follow the steps to install the trivia in your system


## Requirements:

Your system should have installed:

- Node and NPM. [More info](https://nodejs.org/es/download/ "More info")
- Python 3.7. [More info](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python "More info")
- PostgreSQL server. [More info](https://www.postgresql.org/ "More info")
- PIP and Virtual Environment. [More info](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/ "More info")

### Installing Dependencies

Activate your virtual environment and run
```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Configuring your system

Rename the example files and modify them to fit your needs:
```bash
mv .env_example .env
mv .flaskenv_example .flaskenv
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, create database and user running setup.psql and restore a database using the trivia.psql file provided. 

Edit the setup.psql with the desire user info and pass, and run
```bash
psql setup.psql
```

Then, in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run
```
(be sure to configure the .flaskenv file to set environment to dev and flask app to flaskr)

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Reference

**Endpoints**
GET    '/categories'
GET '/questions'
DELETE '/questions/:id'
POST '/questions'
GET '/category/:id/questions'
POST '/quizzes/'

+ **GET '/categories'**
 - **Summary**: Category endpoint.
 - **Description**: Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
 - **Responses:**
 - **200:**
	 - success: True
	 - categories: Categories Array
	 - count: amount of categories
 - **404:**
	 - description: if no categories on db.

&nbsp;

+ **GET '/questions'**
 - **Summary**: return array with questions
 - **Description**: Get paginated questions. If a search string is provided, it will return the seach result.
 + **Parameters**:
      - **page**: int
           - **type**: GET argument
           - **Example**: '?page=1'
           - **Desc**: Page Number
           - **required**: no
      - **question**: string
           - **type**: GET arg: ie '?question=know'
           - **Desc**: Search term. If present it will conduct a search
           - **required**: no
 - **Responses:**
 - **200:**
	 - success: True,
	 - questions: array of formatted questions,
	 - current_page: (int) current page,
	 - total_questions: (int) total questions in db,
	 - categories: format_categories
 - **404:**
	 - success: False,
	 - message: error message.
	 -  code: 404

&nbsp;

+ **DELETE '/questions/:id'**
 - **Summary**: Deletes a question.
 - **Description**:  Seaches for a question based on an id. If found, it deletes the question
 + **Parameters**:
      - **id**: int
           - **type**: path parameter
           - **Example**: '/questions/4'
           - **Desc**: question db id
           - **required**: yes
 - **Responses:**
 - **200:**
	 - success: True
	 - deleted: int with deleted question id
 - **422:**
	 - description: if it can't delete the question or unexisting id.

&nbsp;

+ **POST '/questions/'**
 - **Summary**: Inserts a new question on db.
 - **Description**: Takes vars from a form POST and insert the new question in db
 + **Parameters**:
      - **question**: text
	  - **answer**: text
	  - **difficulty**: int, 1 to 5
	  - **category**: int, category id.
 - **Responses:**
 - **200:**
	 - success: True
	 - created: int with created question id
	 - category: int, category id.
 - **422:**
	 - description: if it can't add the question
+ **Example request**
```
{
    question: "Is the sun a planet?", 
    answer: "no",
    difficulty: 1,
    category: "1"
}
```

&nbsp;

+ **GET '/category/:id/questions'**
 - **Summary**: Questions by category
 - **Description**: Return a list of questions depending on the category
 + **Parameters**:
      - **page**: int
           - **type**: Path parameter
           - **Example**: '/categories/4/questions'
           - **Desc**: category db id
           - **required**: yes
 - **Responses:**
 - **200:**
	 - success: True,
	 - questions: array of formatted questions objects,
	 - current_category: (int) current category,
	 - total_questions: (int) total questions in db,
	 - categories: format_categories
 - **404:**
	 - success: False,
	 - message: error message.
	 -  code: 404

&nbsp;

+ **POST '/quizzes/'**
 - **Summary**: Return a one question
 - **Description**: This endpoint returns a question that belongs to a category, if category is provided and that is not one of the previous questions, according to a previous_question parameter
 + **Parameters**:
      - **quiz_category**: int
           - **type**: POST parameter
           - **Desc**: category db id
           - **required**: yes, but it can be empty
      - **previous_questions**: array
           - **type**: POST parameter
           - **Desc**: array of question ids (integers)
           - **required**: yes, but it can be empty
 - **Responses:**
 - **200:**
	 - success: True,
	 - question: question object, empty if no question left
 - **400:**
	 - success: False,
	 - message: error message.
	 -  code: 400




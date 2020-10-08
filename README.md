# Udacity Category Trivia

Welcome to our fun game of trivia. With this system you'll be able to load default question on setup, add and delete question and play our trivia.

## Requirements:

Our system is a Python/Flask/postgres backend with React frontend, your system should have installed:
- Node and NPM. [More info](https://nodejs.org/es/download/ "More info")
- Python 3.7. [More info](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python "More info")
- PostgreSQL server. [More info](https://www.postgresql.org/ "More info")
- PIP and Virtual Environment. [More info](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/ "More info")


## Install notes:
Follow the steps on the frontend and backend folder to properly install the trivia in your system.

1. [`./frontend/readme.md`](./frontend/README.md)
2. [`./backend/readme.md`](./backend/README.md)

## Enhacements from base project

### Frontend

- I added a CSS framework to help some specific ui details i like to improve
- Changed the size, position and aligment of the menu
- Created (downloaded) a logo
- Changed sizes, spacing, cursor style, etc
- Reworked each question on "list", changed position, added more style
- Modified the search location and style
- Modified the add new trivia

### Backend

- Requirements asked to "*... POST endpoint to get questions based on a search term.*" but i prefer to use **CRUD** recommendations and add the search to the GET request endpoint, and also because I manage to create an entire new behaviour (search question) by just adding a couple of lines of code.


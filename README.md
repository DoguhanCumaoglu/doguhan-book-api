# Book Management API with User Sessions

## Overview

This project is a RESTful API for managing books in a library system, built using FastAPI. The API allows users to perform CRUD (Create, Read, Update, Delete) operations on books and manage user sessions for a personalized experience. The API also implements rate limiting to prevent abuse and uses JWT for user authentication.

## Features

- **Book Management**
  - Retrieve a list of all books
  - Retrieve a specific book by its ID
  - Create a new book (requires user authentication)
  - Update an existing book by its ID (requires user authentication)
  - Delete a book by its ID (requires user authentication)

- **User Management**
  - User registration
  - User login
  - User logout

- **Favorites Management**
  - Mark books as favorites
  - Retrieve the list of favorite books
  - Remove books from favorites

- **Additional Features**
  - Rate limiting
  - JWT-based authentication
  - Proper error handling
  - Pagination for book listings

## Requirements

- Python 3.10+
- FastAPI
- SQLAlchemy
- PostgreSQL (or another SQL database)
- Docker (for deployment)

## Setup Instructions

### Prerequisites

Ensure you have the following installed:
- Python 3.10+
- PostgreSQL (or another SQL database)
- Docker (optional, for deployment)

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/book-management-api.git
    cd book-management-api
    ```

2. **Set Up the Environment**

    Create a `.env` file in the root directory of the project with the following content:

    ```plaintext
    DATABASE_URL=postgresql://user:password@localhost/dbname
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up the Database**

    ```bash
    # Start PostgreSQL server and create a database
    # Replace dbname with your database name

    # Run database migrations
    python -m app.db.database
    ```

5. **Run the Application**

    ```bash
    uvicorn app.main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.

### Docker Setup

1. **Build the Docker Image**

    ```bash
    docker build -t book-management-api .
    ```

2. **Run the Docker Container**

    ```bash
    docker run -e PORT=8000 -p 8000:8000 book-management-api
    ```

### Endpoints

#### Book Endpoints

- `GET /books`: Retrieve a list of all books
- `GET /books/{id}`: Retrieve a specific book by its ID
- `POST /books`: Create a new book (requires authentication)
- `PUT /books/{id}`: Update an existing book by its ID (requires authentication)
- `DELETE /books/{id}`: Delete a book by its ID (requires authentication)

#### User Endpoints

- `POST /register`: Register a new user
- `POST /login`: Log in and receive a JWT token
- `POST /logout`: Log out and invalidate the JWT token

#### Favorites Endpoints

- `GET /favorites`: Retrieve the list of favorite books (requires authentication)
- `POST /favorites/{bookId}`: Add a book to favorites (requires authentication)
- `DELETE /favorites/{bookId}`: Remove a book from favorites (requires authentication)

### CI/CD with GitHub Actions

This project uses GitHub Actions for continuous integration and continuous deployment (CI/CD). The workflow is defined in `.github/workflows/main.yml`.

1. **GitHub Actions Workflow**

    Create a file `.github/workflows/main.yml` with the following content:

    ```yaml
    name: CI/CD Pipeline

    on:
      push:
        branches:
          - main
      pull_request:
        branches:
          - main

    jobs:
      build:
        runs-on: ubuntu-latest

        steps:
        - uses: actions/checkout@v2

        - name: Set up Python
          uses: actions/setup-python@v2
          with:
            python-version: '3.10'

        - name: Install dependencies
          run: |
            python -m pip install --upgrade pip
            pip install -r requirements.txt

        - name: Lint with flake8
          run: |
            pip install flake8
            flake8 .

        - name: Run Tests
          run: |
            pip install pytest
            pytest

      deploy:
        runs-on: ubuntu-latest
        needs: build

        steps:
        - uses: actions/checkout@v2

        - name: Deploy to Heroku
          env:
            HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
            HEROKU_APP_NAME: ${{ secrets.HEROKU_APP_NAME }}
          run: |
            git remote add heroku https://git.heroku.com/${{ secrets.HEROKU_APP_NAME }}.git
            git push heroku main
    ```

2. **GitHub Secrets**

    To securely manage sensitive information, use GitHub Secrets:

    - `HEROKU_API_KEY`: Your Heroku API key.
    - `HEROKU_APP_NAME`: Your Heroku application name.

    To add secrets, go to your GitHub repository, click on `Settings`, then `Secrets`, and then `New repository secret`.

### Testing

To run the tests, use:

```bash
pytest

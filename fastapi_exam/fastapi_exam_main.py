"""
This module implements a FastAPI application for an MCQ (Multiple Choice Questions) API.

Endpoints:
- GET /verify: Verifies the API functionality.
- POST /question: Creates a new question (admin access required).
- GET /mcq: Generates an MCQ with specified test type and categories.
- POST /login: Performs user authentication using basic authentication.

Authentication:
- Basic Authentication: Users need to provide their username and password as a Base64-encoded string in the Authorization header.

Data Models:
- Question: Represents a multiple-choice question with various fields such as the question title, subject, correct answers, and answer options.

Additional Information:
- The 'questions' list is used to store the created questions in memory, but a real-world implementation should use a database or storage solution for persistence.

Author: Thomas Bury
Date: 22/05/2023
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import random
import pandas as pd
from typing import Annotated

api_doc_tags = [
    {
        'name': 'users',
        'description': 'Users endpoints'
    },
    {
        'name': 'admin',
        'description': 'Admin endpoints'
    },
    {
        'name': 'test',
        'description': 'Testing endpoints'
    }
]

api = FastAPI(   
    title="DS fastAPI exam",
    description="MCQ API",
    version="1.0.0",
    openapi_tags=api_doc_tags)

security = HTTPBasic()

users = {
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}

class Question(BaseModel):
    """
    Represents a multiple-choice question.

    Attributes:
        question (str): The title of the question.
        subject (str): The category of the question.
        correct (list[str]): The list of correct answers.
        use (str): The type of MCQ for which this question is used.
        answerA (str): Answer A.
        answerB (str): Answer B.
        answerC (str): Answer C.
        answerD (str): The answer D (if it exists).

    Note:
        - The `question` attribute represents the title or content of the question.
        - The `subject` attribute represents the category or subject of the question.
        - The `correct` attribute is a list of strings representing the correct answers.
        - The `use` attribute represents the type of MCQ (Multiple Choice Questions) for which this question is used.
        - The `answerA`, `answerB`, `answerC`, and `answerD` attributes represent the answer options for the question.
        - The `answerD` attribute is optional and only present if there is a fourth answer option.

    Example:
        {
            "question": "What is the capital of France?",
            "subject": "Geography",
            "correct": ["Paris"],
            "use": "Geography Quiz",
            "answerA": "London",
            "answerB": "Berlin",
            "answerC": "Paris"
        }
    """
    question: str
    subject: str
    correct: list[str]
    use: str
    answerA: str
    answerB: str
    answerC: str
    answerD: str = None
    

def load_questions_from_csv(csv_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path)

    # Convert the DataFrame to a list of dictionaries
    question_dicts = df.to_dict(orient='records')

    # Convert the dictionaries to Question instances
    # there are quality issues with the data types, 
    # so we convert them to strings
    questions = []
    for question_dict in question_dicts:
        question = Question(
            question=question_dict['question'],
            subject=question_dict['subject'],
            correct=str(question_dict['correct']).split(' '),
            use=question_dict['use'],
            answerA=question_dict['responseA'],
            answerB=question_dict['responseB'],
            answerC=question_dict['responseC'],
            answerD=question_dict['responseD'] if pd.notnull(question_dict['responseD']) else None
        )
        questions.append(question)

    return questions
    
    # List to store the created questions
questions = load_questions_from_csv('~/Downloads/questions.csv')  

@api.get("/verify", tags=['test'])
def verify():
    """
    Endpoint to verify the functionality of the API.

    Returns:
        dict: A JSON response indicating that the API is functional.
    """
    return {"message": "API is functional"}

@api.post("/question", tags=['admin'])
def create_question(question: Question, credentials: HTTPBasicCredentials):
    """
    Endpoint to create a new question.

    Args:
        question (Question): The question data provided in the request body.
        credentials (HTTPBasicCredentials): User credentials for authentication.

    Returns:
        dict: A JSON response indicating the successful creation of the question.

    Raises:
        HTTPException: If the provided credentials are unauthorized.
    """
    if credentials.username != "admin" or credentials.password != "4dm1N":
        raise HTTPException(status_code=401, detail="Unauthorized")
    questions.append(question)
    return {"message": "Question created successfully"}

@api.get("/mcq", tags=['users'])
def generate_mcq(test_type: str, categories: Annotated[list[str], Query()], number: int):
    """
    Endpoint to generate an MCQ with the specified parameters.

    Args:
        test_type (str): The type of MCQ for which the questions are generated.
        categories(list(str)): The category of questions to include in the MCQ.
        number (int): The number of questions to include in the MCQ.

    Returns:
        list[Question]: A list of randomly selected questions in JSON format.

    Note:
        The questions are filtered based on the test type and categories, and then a random selection is made.
    """
    if number not in [5, 10, 20]:
        raise HTTPException(status_code=400, detail="Invalid number of questions")
    
    filtered_questions = [q for q in questions if q.use == test_type and q.subject in categories]

    random_questions = random.sample(filtered_questions, number)
    return random_questions

@api.post("/login", tags=['users'])
def login(credentials: HTTPBasicCredentials):
    """
    Endpoint for user authentication.

    Args:
        credentials (HTTPBasicCredentials): User credentials provided in the request.

    Returns:
        dict: A JSON response indicating successful login.

    Raises:
        HTTPException: If the provided credentials are invalid.
    """
    username = credentials.username
    password = credentials.password

    if username in users and users[username] == password:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
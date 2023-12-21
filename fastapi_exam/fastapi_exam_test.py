import requests
import base64

# Set the base URL for the API
base_url = "http://localhost:8000"

# Function to make a GET request to the /verify endpoint
def verify_api():
    response = requests.get(f"{base_url}/verify")
    print(response.json())

# Function to make a POST request to the /login endpoint
def login(username, password):
    data = {
        'username': username,
        'password': password
    }

    response = requests.post(f"{base_url}/login", json=data)
    print(response.json())

# Function to make a POST request to the /question endpoint
def create_question(question_data, credentials):
    
    json_data = {"question": question_data, "credentials": credentials}
    
    response = requests.post(
        f"{base_url}/question",
        json=json_data
    )
    print(response.json())

# Function to make a GET request to the /mcq endpoint
def generate_mcq(test_type, categories, number):
    response = requests.get(
        f"{base_url}/mcq",
        params={"test_type": test_type, "categories": categories, "number": number}
    )
    print(response.json())

# Test the API endpoints
if __name__ == "__main__":
    verify_api()

    # Test user login
    login("alice", "wonderland")

    # Create a new question
    question_data = {
        "question": "What is the capital of France?",
        "subject": "Geography",
        "correct": ["Paris"],
        "use": "Geography Quiz",
        "answerA": "London",
        "answerB": "Berlin",
        "answerC": "Paris"
    }
    credentials = {
        'username': "admin",
        'password': "4dm1N"
    }
    create_question(question_data, credentials)

    # Generate an MCQ
    test_type = "Test de positionnement"
    categories = ["BDD"]
    number = 5
    generate_mcq(test_type, categories, number)

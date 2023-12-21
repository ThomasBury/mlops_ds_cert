# FastAPI exam

## Steps to implement
Goal: create a FastAPI application that handles various endpoints for generating MCQs, user authentication, question creation, and functional verification. High-level outline of the implementation steps:

 - Create a FastAPI application: Set up a new FastAPI application to serve as the foundation for the API.

 - Define the data model: Create a Pydantic model that represents the structure of the question data, including the fields mentioned (question, subject, correct answers, use, answer options) and their data type. This model will be used for request/response validation.

 - Implement user authentication: Add authentication to handle basic authentication. Use the provided dictionary of usernames and passwords for verification.

 - Endpoint for choosing test type and categories: Create an endpoint that allows users to choose the test type (use) and one or more categories (subjects) for the MCQs.

 - Randomly retrieve questions: Implement a mechanism to retrieve the specified number of random questions based on the test type and categories chosen by the user. In order to avoid multiple identical questions.

 - Endpoint for verifying API functionality: Create an endpoint that returns a simple response to verify that the API is functioning correctly.

 - Endpoint for admin user to create a new question: Implement an endpoint that allows an admin user (identified by the password) to create a new question and add it to the dataset.

 - Error handling and documentation: Add appropriate error handling to return meaningful error responses when the API is called incorrectly. Generate API documentation using FastAPI's automatic documentation generation features.

 - Write Python files: Organize the code into separate Python files, such as main.py for the FastAPI application and models.py for the data model. However, since the data model is quite simple, the code can be written in the main module.

 - Write a test command file: Create a file that contains commands to test the API, demonstrating various API calls and their expected responses.

## Architecture

 - FastAPI: FastAPI is chosen as the web framework for building the API due to its high performance, easy-to-use nature, and excellent support for asynchronous programming. FastAPI leverages the power of Python type hints and annotations to provide automatic request/response validation, API documentation generation, and fast execution speed. And also because it is covered by the course material :)

 - Authentication: Basic authentication is used for simplicity. The HTTPBasic security class from FastAPI is used to handle basic authentication. User credentials are passed in the Authorization header, and the provided dictionary is used for verification. Not a real world viable solution.

 - Data Model: The Pydantic library is employed to define a data model for the Question class. Pydantic provides data validation, serialization, and automatic API documentation generation based on Python type hints. It ensures that the incoming and outgoing data rfollows the defined structure.

 - Data Storage: the created questions are stored in a simple list questions. However, in a real life application, a database is a better solution (data persistence, retrieve and manage questions more efficiently).

 - Endpoint Design: Endpoints are defined with appropriate HTTP methods (GET, POST) and paths (/verify, /question, /mcq, /login), following the RESTful principles.

 - Error Handling: FastAPI has exception handling mechanism, used to return appropriate HTTP status codes and error messages when requests are incorrect or unauthorized. The HTTPException class is used to raise exceptions with the desired status codes and details.

 - Modularity: The code should be structured into separate files, such as a models.py file for data models or a utils.py file for utility functions.

 - Documentation: FastAPI/OpenAPI's automatic documentation generation feature is used to generate API documentation based on the defined data models and endpoints. This documentation provides information to API consumers, including the structure of request/response bodies, allowed values, and example requests/responses.


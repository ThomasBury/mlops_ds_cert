# Use the official Python base image with version 3.9
FROM python:3.9

# Set the working directory inside the container
WORKDIR /test

# Copy the Python script to the container
ADD test_authentication.py /test/test_authentication.py

# Install the requests library
RUN pip install requests

# Set the environment variable for logging
ENV LOG=1

# Run the Python script
CMD ["python", "test_authentication.py"]
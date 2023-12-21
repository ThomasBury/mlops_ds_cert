#!/bin/bash

# Build the images
cd ./test_authentication
docker build -t authentication-test .

cd ../test_permission
docker build -t permission-test .

cd ../test_sentiment
docker build -t sentiment-test .

cd ..

chmod -R 777 logs
touch logs/api_test.log
chmod -R 777 logs/api_test.log

# Launch Docker Compose
docker-compose up

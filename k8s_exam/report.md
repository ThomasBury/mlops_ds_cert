# Project Report: Deploying FastAPI and MySQL with Kubernetes

## Overview
The goal of this project was to deploy a FastAPI-based API and a MySQL database using Kubernetes. The deployment involved creating a Deployment with multiple Pods, each containing a FastAPI container and a MySQL container. Additionally, a Service and an Ingress were created to enable access to the API.

## Steps Taken

1. **Docker Configuration**: A Dockerfile was provided, which included installing dependencies, exposing port 8000, and specifying the command to run the FastAPI server. The necessary Python packages were listed in the requirements.txt file. I built the image and pushed it to my Dockerhub repository (dummy-api)

2. **Configuration Files**: Several configuration files were provided for the Kubernetes deployment:

   - `my-deployment-eval.yml`: This file defined a Deployment resource with replicas set to 3. It included the specifications for both the FastAPI container and the MySQL container. The environment variables for the MySQL password were referenced from a Secret. This port for the FastAPI container was set to 8000 as in the docker file.
   
   - `my-service-eval.yml`: This file defined separate Service resources for the FastAPI and MySQL containers. The Services exposed the necessary ports (FastAPI container 8000 to the port 8080 and MySQL container port 3306) to route traffic to the respective containers.
   
   - `my-ingress-eval.yml`: This file defined an Ingress resource to enable external access to the FastAPI service. It included the necessary annotations for rewriting the target URL, using the multiservices configuration, although we expose only the fastapi service.
   
   - `my-secret-eval.yml`: This file defined a Secret resource to store sensitive information, such as the MySQL password. The password was base64-encoded for security.

3. **Updating Configuration Files**: The provided configuration files were updated to address any errors and to separate the services for FastAPI and MySQL. Labels and selectors were applied to ensure proper association between the containers and services.

4. **Applying Configurations**: The updated configuration files were applied to the Kubernetes cluster using the `kubectl apply -f <filename>` command. The Secret, Deployment, Service, and Ingress resources were created in the cluster.

5. **Testing API Accessibility**: The API's accessibility was verified by checking the status endpoint (`/status`). The Ingress IP address or domain name was mapped to the desired hostname in the local machine's hosts file. Then, the API was accessed using a web browser, requesting the appropriate hostname. However, the DB itself cannot be reached. I guess the URL in the `main.py`, set to "mysql-service" is not the right one. I cannot figure out why, despite spending much more time than the "1h" claimed to finish the assessment.
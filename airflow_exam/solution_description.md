# Airflow Exam Report

## Introduction
The Weather Data Pipeline is a data processing workflow designed to retrieve weather data from the OpenWeatherMap API, transform it into a csv format and adding lags, and train a prediction model for temperature (high autocorrelation, timeseries modelling). This report provides an overview of the solution implemented using Airflow and scikit-learn only (other solution might be better than scikit-learn such as ligthgbm, tslearn, prophet, etc.).

## Data Retrieval
The pipeline starts by fetching raw weather data for Paris, Brussels and Amsterdam using the OpenWeatherMap API. The `get_raw_weather_data` function is responsible for making API calls and storing the data in JSON format. The weather data includes temperature, city information, and atmospheric pressure.

## Data Transformation
Once the raw weather data is obtained, it is transformed into a CSV format for further processing. The `transform_data_into_csv` function reads the raw JSON files, extracts relevant information for each city, and creates a dataframe, creating lags of the temperature for the sake of timeseries modelling (AR process). This dataframe is then saved as a CSV file for later use. The transformation process includes selecting specific attributes such as temperature and pressure, associating the data with the corresponding city and date, and organizing it in tabular form.

## Model Training and Evaluation
After data transformation, the pipeline proceeds to train and evaluate different regression models using cross-validation (I replaced the KFold by a proper timeseries split). Three models are used: Linear Regression, Decision Tree Regression, and HGBM. For each model, the `compute_model_score` function performs cross-validation to evaluate the model's performance using the mean squared error metric. The resulting scores are stored in the Airflow task instance's XCom, allowing for easy retrieval and comparison.

## Model Selection
Once the models are evaluated, the `fetch_scores` function fetches the model scores from the XCom and selects the model with the highest score as the winner. The winning model is then retrained using all available data, and the trained model is stored using the joblib library for future use (I change pickle to joblib instead).

## Pipeline Execution and Scheduling
The Weather Data Pipeline is orchestrated using Apache Airflow. It is configured to run every minute. The pipeline, DAG, has dependencies which ensure that the tasks are executed in the correct order. The DAG configuration also includes default arguments such as the owner, start date, retries, and retry delay. I did not include any conditionals here.

## Conclusion
The Weather Data Pipeline provides an automated solution for retrieving weather data, transforming it into a usable format, and training a prediction model. It leverages Apache Airflow to schedule and execute the pipeline tasks, ensuring data processing and model training are performed efficiently and consistently. The modular design allows for easy maintenance, extensibility (other models), and customization.
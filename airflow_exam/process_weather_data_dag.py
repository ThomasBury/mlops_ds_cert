import requests
import json
import os
import pandas as pd
from sklearn.model_selection import cross_val_score, TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from joblib import dump
from datetime import datetime, timedelta
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.models import Variable

# API key
api_key = "YOUR_API_KEY"
cities = ['paris', 'brussels', 'amsterdam']



cities = ['paris', 'brussels', 'amsterdam']
Variable.set("cities", cities)

def get_raw_weather_data(api_key, cities):
    """
    Retrieve raw weather data for the specified cities from the OpenWeatherMap API.

    Args:
        api_key (str): API key for accessing the OpenWeatherMap API.
        cities (list): List of city names to fetch weather data for.

    Returns:
        None
    """
    url = "https://api.openweathermap.org/data/2.5/weather"

    weather_data = {}
    for city in cities:
        params = {"q": city, "appid": api_key, "units": "metric"}
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        weather_data[city] = data

    filename = datetime.now().strftime("%Y-%m-%d %H:%M") + ".json"
    filepath = os.path.join("/app/raw_files", filename)
    with open(filepath, "w") as f:
        json.dump(weather_data, f)
    print("Weather data saved to", filepath)

def transform_data_into_csv(n_files=None, filename='data.csv'):
    """
    Transform the raw weather data into a CSV format.

    Args:
        n_files (int, optional): Number of files to include in the transformation. Default is None.
        filename (str, optional): Name of the output CSV file. Default is 'data.csv'.

    Returns:
        None
    """
    parent_folder = '/app/raw_files'
    files = sorted(os.listdir(parent_folder), reverse=True)[:n_files] if n_files else os.listdir(parent_folder)
    dfs = []

    for file_name in files:
        with open(os.path.join(parent_folder, file_name), 'r') as file:
            data = json.load(file)
        for city, city_data in data.items():
            dfs.append({
                'temperature': city_data['main']['temp'],
                'city': city_data['name'],
                'pressure': city_data['main']['pressure'],
                'date': file_name.split('.')[0]
            })

    df = pd.DataFrame(dfs)
    df.to_csv(os.path.join('/app/clean_data', filename), index=False)
    print(df.head(10))

def compute_model_score(model, **context):
    """
    Compute the cross-validated score for a given regression model.

    Args:
        model: The regression model to evaluate.
        **context: Additional context provided by Airflow.

    Returns:
        None
    """
    X, y = prepare_data('/app/clean_data/fulldata.csv')
    tscv = TimeSeriesSplit(n_splits=3)
    cross_validation = cross_val_score(model, X, y, cv=tscv, scoring='neg_mean_squared_error')
    model_score = cross_validation.mean()
    context['ti'].xcom_push(key=f'{model.__class__.__name__}_score', value=model_score)

def train_model(model, **context):
    """
    Train a regression model on the prepared data.

    Args:
        model: The regression model to train.
        **context: Additional context provided by Airflow.

    Returns:
        The trained regression model.
    """
    X, y = prepare_data('/app/clean_data/fulldata.csv')
    model.fit(X, y)
    return model

def prepare_data(path_to_data='/app/clean_data/fulldata.csv'):
    """
    Prepare the data for model training by creating lagged variables and splitting into features and target.

    Args:
        path_to_data (str, optional): Path to the data CSV file. Default is '/app/clean_data/fulldata.csv'.

    Returns:
        Tuple containing the features and target arrays.
    """
    df = pd.read_csv(path_to_data)
    df = df.sort_values(['city', 'date'], ascending=True)

    # Create lagged variables for temperature
    # using builtin groupby rahter than recoding it using a loop
    for i in range(1, 10):
        df[f'temp_m-{i}'] = df.groupby('city')['temperature'].shift(i)

    # Drop rows with missing values
    df = df.dropna()

    # Split the data into features and target
    features = df.drop(['date', 'target'], axis=1)
    target = df['target']

    return features, target

def fetch_scores(**context):
    """
    Fetch the scores of the trained regression models and select the model with the highest score.

    Args:
        **context: Additional context provided by Airflow.

    Returns:
        None
    """
    gbm_score = context['ti'].xcom_pull(key='HistGradientBoostingRegressor_score')
    lr_score = context['ti'].xcom_pull(key='LinearRegression_score')
    dt_score = context['ti'].xcom_pull(key='DecisionTreeRegressor_score')

    scores = {
        'GBM': gbm_score,
        'Linear Regression': lr_score,
        'Decision Tree': dt_score
    }

    winner = max(scores, key=scores.get)
    model = models[winner]

    trained_model = train_model(model, **context)
    dump(trained_model, '/app/trained_winner.joblib')
    context['ti'].xcom_push(key='winner_model', value=trained_model)
    context['ti'].xcom_push(key='winner', value=winner)


def retrain_and_store_winner(**context):
    """
    Retrain the winning model on all the data and store it.

    Args:
        **context: Additional context provided by Airflow.

    Returns:
        None
    """
    winner_model = context['ti'].xcom_pull(key='winner_model')
    trained_model = train_model(winner_model, **context)
    dump(trained_model, '/app/trained_winner.joblib')





__doc__ = """
weather_data_pipeline DAG

Description:
A DAG to retrieve weather data, transform it, and train a prediction model.

Schedule:
Run every minute.

Tasks:
- get_weather_data_task: Retrieve weather data from the OpenWeatherMap API.
- transform_data_dashboard_task: Transform the weather data into CSV format for the dashboard.
- transform_data_task: Transform the weather data into CSV format for model training.
- xval_model_tasks: Perform cross-validation for each regression model.
- fetch_scores_task: Fetch the scores and select the winning model.
- retrain_and_store_model_task: Retrain and store the winning model.

Dependencies:
- get_weather_data_task depends on nothing.
- transform_data_dashboard_task depends on get_weather_data_task.
- transform_data_task depends on get_weather_data_task.
- xval_model_tasks depend on transform_data_task.
- fetch_scores_task depends on xval_model_tasks.
- retrain_and_store_model_task depends on fetch_scores_task.
"""



default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0, minute=1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'weather_data_pipeline',
    default_args=default_args,
    description='A DAG to retrieve weather data, transform it, and train a prediction model',
    schedule_interval='*/1 * * * *',  # Run every minute
    doc_md=__doc__,
) as dag:

    get_weather_data_task = PythonOperator(
        task_id='get_weather_data',
        python_callable=get_raw_weather_data,
        op_kwargs={'api_key': api_key, 'cities': cities},
    )

    transform_data_dashboard_task = PythonOperator(
        task_id='transform_data_dashboard',
        python_callable=transform_data_into_csv,
        op_kwargs={'n_files': 20, 'filename': 'data.csv'},
    )
    
    transform_data_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data_into_csv,
        op_kwargs={'n_files': None, 'filename': 'data.csv'},
    )

    models = [LinearRegression(), DecisionTreeRegressor(), HistGradientBoostingRegressor()]

    xval_model_tasks = []
    for i, model in enumerate(models):
        xval_model_task = PythonOperator(
            task_id=f'xval_model_{i+1}',
            python_callable=compute_model_score,
            op_kwargs={'model': model},
            provide_context=True,
        )
        xval_model_tasks.append(xval_model_task)

    fetch_scores_task = PythonOperator(
        task_id='fetch_scores',
        provide_context=True,
        python_callable=fetch_scores,
    )

    retrain_and_store_model_task = PythonOperator(
        task_id='retrain_and_store_model',
        provide_context=True,
        python_callable=retrain_and_store_winner,
    )

    get_weather_data_task >> transform_data_dashboard_task
    get_weather_data_task >> transform_data_task

    transform_data_task >> xval_model_tasks

    for xval_model_task in xval_model_tasks:
        xval_model_task >> fetch_scores_task

    fetch_scores_task >> retrain_and_store_model_task

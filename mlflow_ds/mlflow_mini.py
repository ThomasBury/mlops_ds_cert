import mlflow

#define the path in which you want to save the runs
path = "/HOME/Documents/mlops/mlflow_ds/mlruns"
mlflow.set_tracking_uri("file://"+ path)

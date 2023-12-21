import os
import warnings
import sys
import pandas as pd
import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import lasso_path, enet_path
from sklearn import datasets

# Import MLflow
import mlflow
import mlflow.sklearn


experiment_name = "ElasticNet"
current_experiment=dict(mlflow.get_experiment_by_name(experiment_name))
experiment_id=current_experiment['experiment_id']

with mlflow.start_run(experiment_id =experiment_id):

    # datasets loading
    diabetes = datasets.load_diabetes()
    X = diabetes.data
    y = diabetes.target

    # creation of the pandas dataframe
    Y = np.array([y]).transpose()
    d = np.concatenate((X, Y), axis=1)
    cols = diabetes.feature_names + ["progression"]
    data = pd.DataFrame(d, columns=cols)

    # Metrics evaluation
    def eval_metrics(actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2




    if __name__ == "__main__":
        warnings.filterwarnings("ignore")
        np.random.seed(40)

        # Train and test sets: (0.75, 0.25) split.
        train, test = train_test_split(data)

        # target variable is the column "progression" 
        train_x = train.drop(["progression"], axis=1)
        test_x = test.drop(["progression"], axis=1)
        train_y = train[["progression"]]
        test_y = test[["progression"]]


        alpha = 0.7
        l1_ratio = 0.7


        # ElasticNet model
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)
        predicted_qualities = lr.predict(test_x)
        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        # Model metrics
        print("Elasticnet model (alpha=%f, l1_ratio=%f):" )#% (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        # Parameters and metrics loading on MLflow
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        mlflow.sklearn.log_model(lr, "model")

        # Compute paths
        eps = 5e-3  # the smaller it is the longer is the path
        print("Computing regularization path using the elastic net.")
        alphas_enet, coefs_enet, _ = enet_path(X, y, eps=eps, l1_ratio=l1_ratio)

        # Results
        fig = plt.figure(1)
        ax = plt.gca()

        # Model coefficients plot
        colors = cycle(["b", "r", "g", "c", "k"])
        neg_log_alphas_enet = -np.log10(alphas_enet)
        for coef_e, c in zip(coefs_enet, colors):
            l2 = plt.plot(neg_log_alphas_enet, coef_e, linestyle="--", c=c)

        plt.xlabel("-Log(alpha)")
        plt.ylabel("coefficients")
        title = "ElasticNet Path by alpha for l1_ratio = " + str(l1_ratio)
        plt.title(title)
        plt.axis("tight")
        plt.show()

        # Saving plot
        fig.savefig("ElasticNet-paths.png")

        plt.close(fig)

        # artifacts (output files)
        mlflow.log_artifact("ElasticNet-paths.png")
        data.to_csv('diabetes.txt', encoding = 'utf-8', index=False)
        mlflow.log_artifact('diabetes.txt')
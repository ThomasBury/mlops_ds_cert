# import of the necessary packages
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


import mlflow
import mlflow.sklearn

experiment_id = mlflow.create_experiment('ElasticNet')
with mlflow.start_run(experiment_id=experiment_id):

    # data loading
    diabetes = datasets.load_diabetes()
    X = diabetes.data
    y = diabetes.target

    # pandas dataframe creation
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

        # Training and test sets: (0.75, 0.25) split.
        train, test = train_test_split(data)

        # The target variable is the column "progression"
        train_x = train.drop(["progression"], axis=1)
        test_x = test.drop(["progression"], axis=1)
        train_y = train[["progression"]]
        test_y = test[["progression"]]


        alpha = 1
        l1_ratio = 0.5


        # ElasticNet
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)
        predicted_qualities = lr.predict(test_x)
        (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

        # Model metrics
        print(f"Elasticnet model (alpha={alpha:.2f} l1_ratio={l1_ratio:.2f}):" )
        print(f"  RMSE: {rmse:.4f}" )
        print(f"  MAE: {mae:.4f}")
        print(f"  R2: {r2:.4f}")

        # Loading the metrics and MLflow parameters
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

        #plot of the model coefficients
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

        # Saving the plot
        fig.savefig("ElasticNet-paths.png")

        plt.close(fig)

        # artifacts (output files)
        mlflow.log_artifact("ElasticNet-paths.png")
        data.to_csv('diabetes.txt', encoding = 'utf-8', index=False)
        mlflow.log_artifact('diabetes.txt')

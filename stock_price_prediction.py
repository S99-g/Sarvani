# -*- coding: utf-8 -*-
"""Stock Price Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1595rai6mG9VaUGZWw7f0Z_DOidenv42M
"""

pip install pandas numpy scikit-learn matplotlib

pip install pandas numpy scikit-learn tensorflow

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

df = pd.read_csv('/zomato.csv')

print(df.head())


df = df[['Date', 'Close']]
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

features = df[['Close']]

from sklearn.cluster import KMeans


scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)


wcss = []
for i in range(1, 14):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=42)
    kmeans.fit(scaled_features)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 14), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

optimal_clusters = 6
kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=300, n_init=10, random_state=42)
df['Cluster'] = kmeans.fit_predict(scaled_features)

plt.figure(figsize=(19, 7))
for cluster in range(optimal_clusters):
    cluster_data = df[df['Cluster'] == cluster]
    plt.plot(cluster_data.index, cluster_data['Close'], label=f'Cluster {cluster}')

plt.title('Stock Price Clusters')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

models = {}
for cluster in range(optimal_clusters):
    cluster_data = df[df['Cluster'] == cluster][['Close']]
    X = cluster_data.index.factorize()[0].reshape(-1, 1)
    y = cluster_data['Close'].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)

    models[cluster] = model

    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f'Cluster {cluster} RMSE: {rmse}')

predictions = []
for cluster in range(optimal_clusters):
    cluster_data = df[df['Cluster'] == cluster]
    X = cluster_data.index.factorize()[0].reshape(-1, 1)
    model = models[cluster]
    pred = model.predict(X)
    predictions.extend(pred)

df['Prediction'] = np.nan
df.loc[df['Cluster'] == 0, 'Prediction'] = models[0].predict(df[df['Cluster'] == 0].index.factorize()[0].reshape(-1, 1))
df.loc[df['Cluster'] == 1, 'Prediction'] = models[1].predict(df[df['Cluster'] == 1].index.factorize()[0].reshape(-1, 1))
df.loc[df['Cluster'] == 2, 'Prediction'] = models[2].predict(df[df['Cluster'] == 2].index.factorize()[0].reshape(-1, 1))
df.loc[df['Cluster'] == 3, 'Prediction'] = models[3].predict(df[df['Cluster'] == 3].index.factorize()[0].reshape(-1, 1))
df.loc[df['Cluster'] == 4, 'Prediction'] = models[4].predict(df[df['Cluster'] == 4].index.factorize()[0].reshape(-1, 1))
df.loc[df['Cluster'] == 5, 'Prediction'] = models[5].predict(df[df['Cluster'] == 5].index.factorize()[0].reshape(-1, 1))

plt.figure(figsize=(19, 7))
plt.plot(df['Close'], label='Actual Stock Price')
plt.plot(df['Prediction'], label='Predicted Stock Price')
plt.title('Stock Price Prediction using Clustering')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()
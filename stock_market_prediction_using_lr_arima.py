# -*- coding: utf-8 -*-
"""Stock_Market_Prediction_Using_LR_ARIMA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jwkN78VsN4Jt31YWT61fdBsxhAww8zVG
"""

!pip install Quandl

pip install --upgrade yfinance

!pip install pmdarima

import os
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from pmdarima.arima import auto_arima
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math

import pandas as pd #For data related tasks
import matplotlib.pyplot as plt #for data visualization
import quandl #Stock market API for fetching Data
from sklearn.linear_model import LinearRegression

quandl.ApiConfig.api_key = 'm5aYzDNiZMYxQLxso3fb'
stock_data = quandl.get('NSE/TCS', start_date='2018-12-01', end_date='2023-12-1')

print(stock_data)

dataset = pd.DataFrame(stock_data)

dataset.head()
##Now we convert into csv
dataset.to_csv('TCS.csv')

data = pd.read_csv('TCS.csv')

data.head()

# Checking for null values
data.isnull().sum()

# price depend on High,Low,Close,Last,Turnover
x = data.loc[:,'High':'Turnover (Lacs)']
y = data.loc[:,'Open']
x.head()

y.head()

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size = 0.1,random_state = 0)

LR = LinearRegression()

LR.fit(x_train,y_train)

LinearRegression(copy_X=True, fit_intercept=True, n_jobs=None)

LR.score(x_test,y_test)

# test data of random day
Test_data = [[2017.0 ,1979.6 ,1990.00 ,1992.70 ,2321216.0 ,46373.71]]
prediction = LR.predict(Test_data)

print(prediction)



"""**ARIMA**"""

df = yf.download("TCS.NS", period="4y", interval="1d")
df

df = df.asfreq('D')
df

df = df.fillna(method='ffill')
df

ts = df[['Close']]
ts

# Plot the data and identify any unusual observations
plt.figure(figsize=(10, 6))
plt.plot(ts.index, ts.values, label='Original Data')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

from statsmodels.tsa.seasonal import seasonal_decompose
decomposition = seasonal_decompose(ts, model='additive')

trend = decomposition.trend
seasonal = decomposition.seasonal
residuals = decomposition.resid

# Create subplots for each component
fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 8))

# Plot the original time series
axes[0].plot(ts, label='Original')
axes[0].set_ylabel('Original')

# Plot the trend component
axes[1].plot(trend, label='Trend')
axes[1].set_ylabel('Trend')

# Plot the seasonal component
axes[2].plot(seasonal, label='Seasonality')
axes[2].set_ylabel('Seasonality')

# Plot the residuals component
axes[3].plot(residuals, label='Residuals')
axes[3].set_ylabel('Residuals')

# Add titles and legends
axes[0].set_title('Time Series Decomposition')
plt.tight_layout()
plt.show()

from statsmodels.tsa.stattools import adfuller

# Augmented Dickey-Fuller (ADF) Test
result = adfuller(ts)

# Extract p-value from the result
p_value = result[1]

print(p_value)

from pmdarima.arima.utils import ndiffs

ndiffs(ts, test="adf")

from statsmodels.tsa.stattools import adfuller

# Augmented Dickey-Fuller (ADF) Test
result = adfuller(ts.Close.diff().dropna())

# Extract p-value from the result
p_value = result[1]

print(p_value)

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf

fig, ax = plt.subplots(figsize=(10, 6))
plot_acf(ts.Close.diff().dropna(), lags=20, ax=ax)  # Specify the number of lags to display
plt.xlabel('Lag')
plt.ylabel('Autocorrelation')
plt.title('Autocorrelation Function (ACF)')
plt.show()

# train/test split
ts_train = ts.iloc[:int(ts.size * .8)]
ts_test = ts.iloc[int(ts.size * .8):]

# Plot the data and identify any unusual observations
plt.figure(figsize=(10, 6))
plt.plot(ts_train.index, ts_train.values, label='Train Data')
plt.plot(ts_test.index, ts_test.values, 'green', label='Test Data')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

import pmdarima as pm

# Fit the ARIMA model
model = pm.auto_arima(ts_train, seasonal=True)
model.summary()

from statsmodels.tsa.arima.model import ARIMA

# Fit ARIMA model
model = ARIMA(ts_train.values, order=(0, 1, 1))  # Replace p, d, q with appropriate values
model = model.fit()

residuals = pd.DataFrame(model.resid)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 6))

ax1.plot(residuals)
ax2.hist(residuals, density=True)

# Forecast
forecast_steps = int(ts.size) - int(ts.size * .8)  # Number of future time steps to forecas

forecast = model.forecast(steps=forecast_steps)

# Plot the data and identify any unusual observations
plt.figure(figsize=(10, 6))
plt.plot(ts_train.index, ts_train.values, 'blue', label='Train Data')
plt.plot(ts_test.index, ts_test.values, 'green', label='Test Data')
plt.plot(ts_test.index, forecast, 'orange', label='Forecasted Data')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.show()

# Plot the original data and forecasted values
plt.figure(figsize=(10, 6))
plt.plot(ts_test.index, ts_test.values, label='Original Data')
plt.plot(ts_test.index, forecast, label='Forecasted Data')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('ARIMA Forecast')
plt.show()
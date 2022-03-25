import yfinance
import pandas as pd
import seaborn as sns
import numpy as np
from seaborn import regression
from autots import AutoTS
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime
plt.style.use('seaborn-whitegrid')
sns.set()

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-05-01",end="2021-06-29")
df["Dates"] = pd.to_datetime(df.index)
#df['Dates'] = df['Dates'].apply(mpl_dates.date2num)
df = df.loc[:,[ "Dates", 'Open', 'High', 'Low', 'Close']]
df["Close"] = pd.to_datetime(df.index)

print(df)

model = AutoTS(
    forecast_length=10,
    frequency='infer',
    ensemble="simple",
    model_list="superfast",
	transformer_list="fast",
    drop_data_older_than_periods=200
)

model = model.fit(df, date_col='Dates', value_col='Close')



prediction = model.predict()
forecast = prediction.forecast
print("DogeCoin Price Prediction")
print(forecast)
'''

prediction = model.predict()
# Print the details of the best model
print(model)

# point forecasts dataframe
forecasts_df = prediction.forecast
# upper and lower forecasts
forecasts_up, forecasts_low = prediction.upper_forecast, prediction.lower_forecast

# accuracy of all tried model results
model_results = model.results()
# and aggregated from cross validation
validation_results = model.results("validation")

print(model_results)
'''

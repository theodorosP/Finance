import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
from fbprophet import Prophet
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-01-15",end="2021-07-26")
df["Date"] = pd.to_datetime(df.index)
#df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df.describe())

plt.rcParams["figure.figsize"] = [12, 7]
plt.rc("font", size = 14)
#fig , ax = plt.subplots()
#ax.plot(df["Close"])
#date_format = mpl_dates.DateFormatter('%d %b %Y')
#ax.xaxis.set_major_formatter(date_format)
#fig.autofmt_xdate() 
#plt.show()

df = df[["Date", "Close"]]
df = df.rename(columns = {"Date":"ds","Close":"y"})
print(df)


a = np.arange (1.1111111, 1.4, 0.0001)

l = []
for i in a:
	l.append(i)

m = Prophet(interval_width = 0.95, weekly_seasonality = True, yearly_seasonality = True, daily_seasonality = True, changepoint_prior_scale =0.0015 ) 
m.add_seasonality( name='daily',period= 30.5, fourier_order=25)
m.fit(df)
future = m.make_future_dataframe(periods=7, include_history=True)
prediction = m.predict(future)
m.plot(prediction)
plt.title("Prediction of the Doge Coin using the Prophet")
plt.xlabel("Date")
plt.ylabel("Close Stock Price")
plt.show()

#m.plot_components(prediction)
#plt.show()


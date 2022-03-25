import yfinance
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-03-01",end="2021-07-28")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)

lookback = 4
l = []
for i in range(len(df)):
	try:
		 l.append((df["Close"][i] - min(df["Close"][i - lookback + 1: i +1]))/ (max(df["Close"][i - lookback + 1: i +1]) - min(df["Close"][i - lookback + 1: i +1])))
		 print("close = ", df["Close"][i])
		 print("min = ", min(df["Close"][i - lookback + 1: i +1]))
		 print("max = ", (max(df["Close"][i - lookback + 1: i +1])))
	except ValueError:
		pass
print(l)
df = df[3:]
df["Normalizer"] = l
print(df)

plt.rcParams["figure.figsize"] = [12, 7]
plt.rc("font", size = 14)
fig, (ax1, ax2) = plt.subplots(2)
candlestick_ohlc(ax1 ,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8) 
ax2.plot(df["Normalizer"],color = "blue", label = "Normalizer" )
ax2.legend(loc = "upper left")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
plt.show()


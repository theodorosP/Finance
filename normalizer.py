import yfinance
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-01-01",end="2021-07-28")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)
look_back = 50
df['min'] = df['Close'].rolling(look_back).min()
df['max'] = df['Close'].rolling(look_back).max()
df = df[look_back -1:]
print(df)
df["norm"] = (df["Close"] - df["min"])/(df["max"] - df["min"])
print(df)

plt.rcParams["figure.figsize"] = [12, 7]
plt.rc('font', size=14)
fig, (ax1, ax2) = plt.subplots(2)
candlestick_ohlc(ax1,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8) 
ax2.plot(df["norm"], linestyle = "-", color = "blue", label = "normalizer")
ax2.axhline(0.05, linestyle = "--", color = "black")
ax2.axhline(0.95, linestyle = "--", color = "black")
ax2.legend(loc = "best")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
plt.show()

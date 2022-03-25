import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-02-1",end="2021-07-28")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)

period = 21
df["average"] = df["Close"].rolling(period).mean()
df["std"] = df["Close"].rolling(period).std()
print(df)
df = df[period-1:]
print(df)
df["z"] = (df["Close"] - df["average"])/df["std"]
print(df)

plt.rcParams["figure.figsize"] = [12, 7]
plt.rc("font", size = 14)
fig, (ax1, ax2) = plt.subplots(2)
candlestick_ohlc(ax1,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8) 
ax2.plot(df["z"], color = "blue", label ="Z")
ax2.legend(loc = "best")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
plt.axhline(y = 2, color = "red")
plt.axhline(y = -2, color = "red")
fig.autofmt_xdate() 
plt.show()


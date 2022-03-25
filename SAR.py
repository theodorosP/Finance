import yfinance
import pandas as pd
import talib
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-03-1",end="2021-06-30")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)
sar = talib.SAR(df['High'], df['Low'], 0.02)
df["sar"] = sar
print(df)

plt.rcParams["figure.figsize"] = [12, 7]
plt.rc("font", size = 14)

fig, ax = plt.subplots()
candlestick_ohlc(ax,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8) 
ax.plot(df["sar"]) 
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
plt.show()

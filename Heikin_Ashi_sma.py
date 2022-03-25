import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-03-10",end="2021-07-10")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)
lookback_ten = 10
lookback_twenty = 20
df["sma_10"] = df["Close"].rolling(lookback_ten).mean()
df["sma_20"] = df["Close"].rolling(lookback_twenty).mean()
df = df[lookback_twenty -1:]
print(df)

plt.rcParams["figure.figsize"] = [12, 7]
plt.rc("font", size = 14)
fig, ax = plt.subplots()
candlestick_ohlc(ax,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8)
ax.plot(df["sma_10"], linestyle = "-", color = "blue", label = "SMA-10")
ax.plot(df["sma_20"], linestyle = "-", color = "red", label = "SMA-20")
ax.legend(loc = "best")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
plt.show()

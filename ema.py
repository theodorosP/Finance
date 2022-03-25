import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-01",end="2021-07-26")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)
lookback = 1

df['ema12'] = df['Close'].ewm(span=12, adjust=False).mean()
df['ema26'] = df['Close'].ewm(span=26, adjust=False).mean()


plt.rcParams["figure.figsize"] = [12, 7]
plt.rc('font', size=14)
fig, ax = plt.subplots()
candlestick_ohlc(ax,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8) 
ax.plot(df["ema12"], linestyle = "-", color = "blue", label = "ema12")
ax.plot(df["ema26"], linestyle = "-", color = "red", label = "ema26")
ax.legend(loc = "best")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
plt.show()


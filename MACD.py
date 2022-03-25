import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-05-19",end="2021-07-28")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]


'''
fig, ax = plt.subplots()  
ax.plot(df["Close"], label = "Close")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
fig.tight_layout() 
plt.show()

'''
exp1 = df["Close"].ewm(span=12, adjust=False).mean()
exp2 = df["Close"].ewm(span=26, adjust=False).mean()
macd = exp1-exp2
exp3 = macd.ewm(span=9, adjust=False).mean()



'''
fig, ax = plt.subplots()  
ax.plot(macd, label = "macd", color = "red")
ax.plot(exp3, label = "signal", color = "blue")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
ax.legend()
fig.autofmt_xdate() 
fig.tight_layout() 
plt.show()
'''
plt.rcParams['figure.figsize'] = [12, 7]
fig, (ax1, ax2, ax3) = plt.subplots(3)
ax1.plot(df["Close"], label = "Close")
ax2.plot(df["Close"], label = "Close")
ax2.plot(macd, label = "macd", color = "red")
ax2.plot(exp3, label = "signal", color = "blue")
ax3.plot(macd, label = "macd", color = "red")
ax3.plot(exp3, label = "signal", color = "blue")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
for i in[ax1, ax2, ax3]:
	i.legend()
plt.show()



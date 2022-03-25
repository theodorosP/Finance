import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-06-01",end="2021-07-19")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

bulish = []
bearish =[]

for i in range(1, len(df)):
	if df["High"][i] < df["High"][i-1] and df["Low"][i] < df["Low"][i-1] and df["Close"][i] < df["High"][i-1]:
		bulish.append(df["Close"][i])
		bearish.append(np.nan)
	elif df["High"][i] > df["High"][i-1] and df["Low"][i] > df["Low"][i-1] and df["Close"][i] > df["High"][i-1]:
		bulish.append(np.nan)
		bearish.append(df["Close"][i])
	else:
		bearish.append(np.nan)
		bulish.append(np.nan)
bulish.append(np.nan)
bearish.append(np.nan)

df["Buy"] = bulish
df["Sell"] = bearish

print(df) 

fig , (ax)= plt.subplots()
fig.suptitle("TD \n Strategy")
ax.plot(df['Close'], label = "Close")
ax.scatter(df.index, df['Buy'], color='green', label='Buy Signal', marker='^', alpha = 1)
ax.scatter(df.index, df['Sell'], color='red', label='Sell Signal', marker='v', alpha = 1)
plt.legend(loc = "best")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
plt.show()


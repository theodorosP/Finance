import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime
import numpy as np

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(start="2021-01-1",end="2021-07-26")
df["Date"] = pd.to_datetime(df.index)
#df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)

l_up = []
l_down = []
period = 60
for i in range(len(df)):
	try:
		l_up.append(max(df["High"][i - period: i + 1]))
	except ValueError:
		l_up.append(np.nan)

for i in range(len(df)):
	try:
		l_down.append(min(df["Low"][i- period: i + 1]))
	except ValueError:
		l_down.append(np.nan)

df["up"] = l_up
df["down"] = l_down


l_median = []
for i in range (len(df)):
	try:
		l_median.append((df["up"][i] + df["down"][i]) /2)
	except ValueError:
		pass
df["median"] = l_median
df = df[period:]
plt.plot(df["Close"])
plt.plot(df["up"], color = "green", label = "up")
plt.plot(df["median"], label = "median", linestyle = "--")
plt.plot(df["down"], color = "red", label = "down")
plt.legend(loc = "best")
plt.show()

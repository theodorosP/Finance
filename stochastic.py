import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-03-1",end="2021-07-15")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]


df['14-high'] = df['High'].rolling(14).max()
df['14-low'] = df['Low'].rolling(14).min()
print(df)

df['%K'] = (df['Close'] - df['14-low'])*100/(df['14-high'] - df['14-low'])
df['%D'] = df['%K'].rolling(3).mean()
df["diff"] = df["%K"] - df["%D"]
df = df[15:]


l_down = []
l_up = []
for i in range(0, len(df)):
	if df["%K"][i] > df["%D"][i]:
		l_up.append(df["diff"][i])
		l_down.append(np.nan)
	elif df["%K"][i] < df["%D"][i]:
		l_up.append(np.nan)
		l_down.append(df["diff"][i])
	else:
		l_up.append(np.nan)
		l_down.append(n.nan)
df["up"] =l_up
df["down"] = l_down




print(df)
plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)


fig, ax =plt.subplots()

ax.plot(df["diff"])
ax.plot(df["up"],  color = "green")
ax.plot(df["down"],  color = "red")
plt.show()


fig, (ax1, ax2, ax3) = plt.subplots(3)
candlestick_ohlc(ax1,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
ax2.plot(df["%K"], linestyle = "-", color = "blue", label = "%K")
ax2.plot(df["%D"], linestyle = "-", color = "orange", label = "%D")
ax2.axhline(80, linestyle='--', color = 'red')
ax2.axhline(20, linestyle='--', color = 'red')
ax3.plot(df["diff"], linestyle = "-", color = "blue", label = "%K - %D")
ax3.plot(df["up"],  color = "green")
ax3.plot(df["down"], color = "red")
#fix the date
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
ax3.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
ax2.legend(loc = "upper left")
ax3.legend(loc = "upper left")
plt.show()


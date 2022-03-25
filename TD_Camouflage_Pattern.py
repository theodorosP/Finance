import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-03-01",end="2021-07-12")
print(df)
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)
l_true_low = []
l_true_high = []
for i in range(len(df)):
	l_true_low.append( min(df["Low"][i], df["Close"][i-1]))
	l_true_high.append(max(df["High"][i], df["Close"][i-1]))
print("-"*80)		
print(l_true_low)
print("-"*80)		
print(l_true_high)

		
df["true_low"] = l_true_low
		
df["true_high"] = l_true_high



print(df)

bulish = []
bearish = []
#Bulish signal
for i in range(1,  len(df)):
	if df["Close"][i] < df["Close"][i-1] and df["Close"][i] > df["Open"][i] and df["Low"][i] < df["true_low"][i-2]:
		bulish.append(df["Close"][i])
		bearish.append(np.nan)
	elif df["Close"][i] > df["Close"][i] and df["Close"][i] < df["Open"][i] and df["Low"][i] > df["High"][i-2]:
		bulish.append(np.nan)
		bearish.append(df["Close"][i])
	else:
		bulish.append(np.nan)
		bearish.append(np.nan)
		
		


a = np.nan
bulish.append(a)
bearish.append(a)

df["Buy"] = bulish
df["Sell"] = bearish

for i in range(len(df)):
	print(df["Buy"][i])
	print(df["Sell"][i])


'''
fig , (ax)= plt.subplots()


ax.plot(df["Close"], label = "Close", color = "blue")
ax.plot(df['Buy'], color='green', label='Buy Signal', marker='^', alpha = 1)
#ax.scatter(df.index, df['Sell'], color='red',  label='Sell Signal', marker='v', alpha = 1)


#fix the date
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
ax.legend()
fig.text(0.5, 0.03, "Dates", ha="center")
fig.text(0.04, 0.5, "Doge Coin", va = "center", rotation = "vertical")
plt.show()

'''

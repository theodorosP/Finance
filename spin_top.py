import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(start="2021-01-1",end="2022-03-25")
df["Date"] = pd.to_datetime(df.index)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)


def fun(df, body, wick):
	l_buy = []
	l_sell = []
	for i in range(1, len(df)):
		if 	df["Close"][i] - df["Open"][i] < body and \
			df["High"][i] - df["Close"][i] >= wick and\
			df["Open"][i] - df["Low"][i] >= wick and\
			df["Close"][i] > df["Open"][i] and\
			df["Close"][i-1] < df["Open"][i-1]:
				l_buy.append(df["Close"][i])
				l_sell.append(np.nan)
		elif  abs(df["Open"][i] - df["Close"][i]) < body and\
			df["High"][i] - df["Open"][i] >= wick and\
			df["Close"][i] - df["Low"][i] >= wick and\
			df["Close"][i] < df["Open"][i] and\
			df["Close"][i-1] > df["Open"][i-1]:
				l_buy.append(np.nan)
				l_sell.append(df["Close"][i])
		else:
			l_buy.append(np.nan)
			l_sell.append(np.nan)
	l_buy.append(np.nan)
	l_sell.append(np.nan)
	df["Buy"] = l_buy
	df["Sell"] = l_sell
	print(df)
	for i in range(len(df)):
		print(df["Buy"][i])
	print("*"*80)
	for i in range(len(df)):
		print(df["Sell"][i])
	print("*"*80)
	#'''
	fig, ax = plt.subplots()
	ax.plot(df["Close"])
	ax.scatter(df.index, df["Buy"],color='green', label='Buy Signal', marker='^', alpha = 1)
	ax.scatter(df.index, df["Sell"],color='red', label='Sell Signal', marker='v', alpha = 1)
	date_format = mpl_dates.DateFormatter('%d %b %Y')
	ax.xaxis.set_major_formatter(date_format)
	fig.autofmt_xdate() 
	plt.show()
	#'''
	return df
	
'''	
a = np.arange (0.001, 0.01, 0.0001)

l = []
for i in a:
	l.append(i)
for i in l:
	fun(df, 0.02, i)	
'''

fun(df, 0.005, 0.001)
	
	

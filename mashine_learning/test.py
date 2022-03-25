import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
from fbprophet import Prophet
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-15",end="2021-06-03")
df["Date"] = pd.to_datetime(df.index)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

'''
plt.rcParams["figure.figsize"] = [12, 7]
plt.rc("font", size = 14)
df = df[["Date", "Close"]]
df = df.rename(columns = {"Date":"ds","Close":"y"})
print(df)
'''

period = 60
l = []
for i in range(len(df)):
	try:
		l.append( max(df["High"][i - period:i + 1]))
	except ValueError:
		pass
print(l)
df["calc"] = l
print(df)

print(df.shift(1))
df['3day MA'] = df['Close'].shift(1).rolling(window = 3).mean()
df['try'] = df['Close'].rolling(window = 3).mean()

print(df)

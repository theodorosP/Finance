import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime
import numpy as np

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-1",end="2021-06-22")
#print(df.index)
#make index column
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
#use all rows and the mentioned columns
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

print(len(df))
print(df)


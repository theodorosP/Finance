import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-02-1",end="2021-07-26")
df["Date"] = pd.to_datetime(df.index)
#df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]


for i in range(len(df)):
	print(df["Date"][i], "Open", df["Open"][i])
	print(df["Date"][i] ,"Close", df["Close"][i])
	print(df["Date"][i], "High", df["High"][i])
	print(df["Date"][i], "Low", df["Low"][i])



df1 = ticker.history(interval="1d",start="2021-02-1",end="2021-07-26")
df1["Date"] = pd.to_datetime(df1.index)
df1['Date'] = df1['Date'].apply(mpl_dates.date2num)
df1 = df1.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]	

fig, ax = plt.subplots()  
candlestick_ohlc(ax,df1.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
fig.tight_layout()
plt.show()

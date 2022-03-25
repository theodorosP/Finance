import pandas as pd
import numpy as np
import yfinance
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)

name = 'DOGE-USD'
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-01", end="2021-07-30", index_col = "Date")
#first = df[["Open", "High", "Low", "Close"]]

df['Date'] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)

def isSupport(df,i):
	support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < 		df['Low'][i-2]  
	return support
  
def isResistance(df,i):
	resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and 		df['High'][i-1] > df['High'][i-2]  
	return resistance
	
levels = []
for i in range(2,df.shape[0]-2):
	if isSupport(df,i):
		levels.append((i,df['Low'][i]))
	elif isResistance(df,i):
		levels.append((i,df['High'][i]))


fig, ax = plt.subplots()  
candlestick_ohlc(ax,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
fig.tight_layout() 
for level in levels:
	plt.hlines(y = level[1],xmin=df['Date'][level[0]],
	xmax=max(df['Date']),colors='blue')
#plt.savefig("sdf.png")
plt.show()




import pandas as pd
import numpy as np
import yfinance
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from matplotlib.dates import drange

plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)

name = 'DOGE-USD'
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-05-1", end="2021-07-26", index_col = "Date")

data = pd.to_datetime(df.index)
df1 = pd.DataFrame(data)

date_format = mpl_dates.DateFormatter('%d %b %Y')



#first = df[["Open", "High", "Low", "Close"]]

df['Date'] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]

print(df)
print(df.values)



fig, ax = plt.subplots()  
candlestick_ohlc(ax,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
fig.tight_layout() 
#plt.savefig("candles.png")

	
	
	
	
fig , (ax1, ax2)= plt.subplots(2)
fig.suptitle("Real values \n Candles")



ax1.plot(df['Close'], linestyle = "-", label = "Closing Values", color = "green")
candlestick_ohlc(ax2, df.values,width=0.6, colorup='green', colordown='red', alpha=0.8)

#fix the date
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 


fig.text(0.5, 0.03, "Dates", ha="center")
fig.text(0.04, 0.5, "Doge Coin", va = "center", rotation = "vertical")



for ax in [ax1]:
        ax.legend(loc = "best")
        ax.label_outer()


plt.legend()
plt.show()

for i in range(len(df)):
	print(df["Date"][i], "Open", df["Open"][i])
	print(df["Date"][i] ,"Close", df["Close"][i])
	print(df["Date"][i], "High", df["High"][i])
	print(df["Date"][i], "Low", df["Low"][i])
	

import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime
import numpy as np

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-1",end="2021-06-23")
#print(df.index)
#make index column
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
#use all rows and the mentioned columns
df1 = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

period = 20
multiplier = 2
df['UpperBand'] = df['Close'].rolling(period).mean() + df['Close'].rolling(period).std() * multiplier
df['LowerBand'] = df['Close'].rolling(period).mean() - df['Close'].rolling(period).std() * multiplier

df["average"] = df["Close"].rolling(period).mean()


df2 = df1.tail(df1.shape[0] - period)


def get_rsi(close, lookback):
    ret = close.diff()
    up = []
    down = []
    for i in range(len(ret)):
        if ret[i] < 0:
            up.append(0)
            down.append(ret[i])
        else:
            up.append(ret[i])
            down.append(0)
    up_series = pd.Series(up)
    down_series = pd.Series(down).abs()
    up_ewm = up_series.ewm(com = lookback - 1, adjust = False).mean()
    down_ewm = down_series.ewm(com = lookback - 1, adjust = False).mean()
    rs = up_ewm/down_ewm
    rsi = 100 - (100 / (1 + rs))
    rsi_df = pd.DataFrame(rsi).set_index(close.index)   
    rsi_df = rsi_df.dropna()
    return rsi_df[3:]



df['rsi_14'] = get_rsi(df['Close'], 14)
df = df.dropna()
df = df.loc[:,["Date", "Open", "High", "Low", "Close", "Volume", "rsi_14", "UpperBand","LowerBand", "average" ]]

print(df)





plt.rcParams['figure.figsize'] = [12, 7]

plt.rc('font', size=14)

fig, ax = plt.subplots()  
candlestick_ohlc(ax,df2.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
fig.tight_layout() 

plt.plot(df["average"], label = "average")
plt.plot(df['UpperBand'], label = "Upper Bollinger Band")
plt.plot(df['LowerBand'], label = "Lower Bollinger Band")

plt.legend()

plt.show()









fig , (ax1, ax2)= plt.subplots(2)
fig.suptitle("Bolinger Bands \n RSI")



candlestick_ohlc(ax1,df2.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
#date_format = mpl_dates.DateFormatter('%d %b %Y')
#ax.xaxis.set_major_formatter(date_format)
#fig.autofmt_xdate() 
#fig.tight_layout() 

ax1.plot(df["average"], label = "average")
ax1.plot(df['UpperBand'], label = "Upper Bollinger Band")
ax1.plot(df['LowerBand'], label = "Lower Bollinger Band")

plt.legend(loc = "best")


ax2.plot(df["rsi_14"])
plt.axhline(50, linestyle='--', color = 'orange')
date_format = mpl_dates.DateFormatter('%d %b %Y')


#fix the date
date_format = mpl_dates.DateFormatter('%d %b %Y')
#ax1.xaxis.set_major_formatter(date_format)
#ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 


fig.text(0.5, 0.03, "Dates", ha="center")
fig.text(0.04, 0.5, "Doge Coin", va = "center", rotation = "vertical")



plt.show()






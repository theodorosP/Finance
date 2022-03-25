import numpy as np
import pandas as pd
import yfinance
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import datetime
from matplotlib.dates import drange


name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval = "1d", start = "2021-04-1", end="2021-07-21")

#print(df.columns)
df["Date"] = pd.to_datetime(df.index)
df["Date"] = df["Date"].apply(mpl_dates.date2num)
df = df.loc[:,["Date", "Open", "High", "Low", "Close", "Volume"]]

print(df)






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
df = df.loc[:,["Date", "Open", "High", "Low", "Close", "Volume", "rsi_14"]]

print(df)




def implement_rsi_strategy(prices, rsi):    
    buy_price = []
    sell_price = []
    rsi_signal = []
    signal = 0

    for i in range(len(rsi)):
        if rsi[i-1] > 30 and rsi[i] < 30:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
        elif rsi[i-1] < 70 and rsi[i] > 70:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                rsi_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                rsi_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            rsi_signal.append(0)
            
    return buy_price, sell_price, rsi_signal
            

buy_price, sell_price, rsi_signal = implement_rsi_strategy(df['Close'], df['rsi_14'])

print(df.index)










fig, (ax1, ax2) = plt.subplots(2)  
candlestick_ohlc(ax1,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8) 
ax2.plot(df["rsi_14"], color = "orange") 

date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
ax1.plot(df.index, buy_price, marker = '^', markersize = 10, color = 'green', label = 'BUY SIGNAL')
ax1.plot(df.index, sell_price, marker = 'v', markersize = 10, color = 'r', label = 'SELL SIGNAL')

ax2.axhline(30, linestyle = '--', linewidth = 1.5, color = 'grey')
ax2.axhline(50, linestyle = '--', linewidth = 1.5, color = 'blue')
ax2.axhline(70, linestyle = '--', linewidth = 1.5, color = 'grey')
ax1.set_title("Closing price")
ax2.set_title("RSI index")
fig.autofmt_xdate() 
fig.tight_layout()
plt.show()

















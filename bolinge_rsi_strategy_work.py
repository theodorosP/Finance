import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime
import numpy as np

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-03-20",end="2021-06-22")
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
df = df.loc[:,["Date", "Open", "High", "Low", "Close", "Volume", "rsi_14", "UpperBand","LowerBand", "average" ]]



period = 14
limited_df = pd.DataFrame()
limited_df = df[period:]
limited_df["rsi"] = df["rsi_14"]


def get_signal(data, high, low):
	buy_signal = []
	sell_signal = []
	for i in range(len(data['rsi'])):
		if data['rsi'][i] > high:
			buy_signal.append(np.nan)
			sell_signal.append(data['Close'][i])
		elif data['rsi'][i] < low:
			buy_signal.append(data['Close'][i])
			sell_signal.append(np.nan)
		else:
			sell_signal.append(np.nan)
			buy_signal.append(np.nan)

	return (buy_signal, sell_signal)
# Add new columns for Buy and Sell
limited_df['Buy'] = get_signal(limited_df, 80, 20)[0]
limited_df['Sell'] = get_signal(limited_df, 80, 20)[1]



print(limited_df)

limited_df = limited_df.dropna(subset=['Sell'])
print(limited_df)




fig , (ax1, ax2)= plt.subplots(2)
fig.suptitle("Bolinger Bands \n RSI")



candlestick_ohlc(ax1,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  

ax1.plot(df["average"], label = "average")
ax1.plot(df['UpperBand'], label = "Upper Bollinger Band")
ax1.plot(df['LowerBand'], label = "Lower Bollinger Band")
#ax1.scatter(limited_df.index, limited_df['Buy'], color='green', label='Buy Signal', marker='^', alpha = 1)
ax1.scatter(limited_df.index, limited_df['Sell'], color='red', label='Sell Signal', marker='v', alpha = 1)
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



import yfinance
import pandas as pd
import numpy as np
import talib
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime
import numpy as np

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-01",end="2021-07-19")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]


#stochastic
df['14-high'] = df['High'].rolling(14).max()
df['14-low'] = df['Low'].rolling(14).min()
df['%K'] = (df['Close'] - df['14-low'])*100/(df['14-high'] - df['14-low'])
df['%D'] = df['%K'].rolling(3).mean()

#SAR
sar = talib.SAR(df['High'], df['Low'], 0.02)
df["sar"] = sar

#bolinger bands
for i in range(df.shape[0]):
	if i > 0:
		df.loc[df.index[i],'Open'] = (df['Open'][i-1] + df['Close'][i-1])/2
	df.loc[df.index[i],'Close'] = (df['Open'][i] + df['Close'][i] + df['Low'][i] +  df['High'][i])/4
period = 20
multiplier = 2
df['UpperBand'] = df['Close'].rolling(period).mean() + df['Close'].rolling(period).std() * multiplier
df['LowerBand'] = df['Close'].rolling(period).mean() - df['Close'].rolling(period).std() * multiplier
df["average"] = df["Close"].rolling(period).mean()
df["diff"] = df["UpperBand"] - df["LowerBand"]

#rsi
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

bulish = []
bearish =[]

for i in range(1, len(df)):
	if df["High"][i] < df["High"][i-1] and df["Low"][i] < df["Low"][i-1] and df["Close"][i] < df["High"][i-1]:
		bulish.append(df["Close"][i])
		bearish.append(np.nan)
	elif df["High"][i] > df["High"][i-1] and df["Low"][i] > df["Low"][i-1] and df["Close"][i] > df["High"][i-1]:
		bulish.append(np.nan)
		bearish.append(df["Close"][i])
	else:
		bearish.append(np.nan)
		bulish.append(np.nan)
bulish.append(np.nan)
bearish.append(np.nan)

df["Buy"] = bulish
df["Sell"] = bearish
print(df)



df = df[period-1:]
print(df)

plt.rcParams["figure.figsize"] = [12, 7]
plt.rc("font", size = 14)
fig1, ax1 = plt.subplots()
candlestick_ohlc(ax1,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8) 
ax1.plot(df["sar"], color = "blue", linestyle = "-", label = "SAR")
ax1.legend(loc = "best")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
fig1.autofmt_xdate() 
plt.show()


fig2, (ax2, ax3, ax4, ax5, ax6) = plt.subplots(5)
candlestick_ohlc(ax2,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8) 
ax2.plot(df["UpperBand"])
ax2.plot(df["LowerBand"])
ax2.plot(df["average"])
ax3.plot(df["Close"], label = "Close")
ax3.scatter(df.index, df['Buy'], color='green', label='Buy Signal', marker='^')
ax3.scatter(df.index, df['Sell'], color='red', label='Sell Signal', marker='v')
ax4.plot(df["rsi_14"])
ax4.axhline(y = 50, linestyle = "--", color = "orange")
ax5.plot(df["diff"])
ax6.plot(df["%K"], color = "blue", label = "%K")
ax6.plot(df["%D"], color = "orange", label = "%D")
ax6.axhline(y = 20, linestyle = "--", color = "red")
ax6.axhline(y = 80, linestyle = "--", color = "red")
for ax in [ax3, ax6]:
	ax.legend(loc = "upper left")
date_format = mpl_dates.DateFormatter('%d %b %Y')
fig2.autofmt_xdate() 
plt.show()




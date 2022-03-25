import yfinance
import pandas as pd
import talib
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-03-15",end="2021-07-30")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)

#stochastic
df['14-high'] = df['High'].rolling(14).max()
df['14-low'] = df['Low'].rolling(14).min()
df['%K'] = (df['Close'] - df['14-low'])*100/(df['14-high'] - df['14-low'])
df['%D'] = df['%K'].rolling(3).mean()
df["diff"] = df["%K"] - df["%D"]
print(df)

#SAR
sar = talib.SAR(df['High'], df['Low'], 0.02)
df["sar"] = sar
print(df)

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
print(df)

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
print(df)

#ADX
def get_adx(high, low, close, lookback):
	plus_dm = high.diff()
	minus_dm = low.diff()
	plus_dm[plus_dm < 0] = 0
	minus_dm[minus_dm > 0] = 0
	tr1 = pd.DataFrame(high - low)
	tr2 = pd.DataFrame(abs(high - close.shift(1)))
	tr3 = pd.DataFrame(abs(low - close.shift(1)))
	frames = [tr1, tr2, tr3]
	tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
	atr = tr.rolling(lookback).mean()
	plus_di = 100 * (plus_dm.ewm(alpha = 1/lookback).mean() / atr)
	minus_di = abs(100 * (minus_dm.ewm(alpha = 1/lookback).mean() / atr))
	dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
	adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
	adx_smooth = adx.ewm(alpha = 1/lookback).mean()
	return plus_di, minus_di, adx_smooth

df['plus_di'] = get_adx(df['High'], df['Low'], df['Close'], 14)[0]
df['minus_di'] = get_adx(df['High'], df['Low'], df['Close'], 14)[1]
df['adx'] = get_adx(df['High'], df['Low'], df['Close'], 14)[2]
l_up_trend = []
l_down_trend = []
for i in range(0, len(df)):
	if df["adx"][i] > 25 and df["plus_di"][i] > df["minus_di"][i]:
		l_up_trend.append(df["Close"][i])
		l_down_trend.append(np.nan)
	elif df["adx"][i] > 25 and df["plus_di"][i] < df["minus_di"][i]:
		l_up_trend.append(np.nan)
		l_down_trend.append(df["Close"][i]) 
	else:
		l_up_trend.append(np.nan)
		l_down_trend.append(np.nan)
df["up_trend"] = l_up_trend
df["down_trend"] = l_down_trend
print(df) 


df = df[19:]
print(df)
plt.rcParams["figure.figsize"] = [12, 7]
plt.rc("font", size = "14")
fig, (ax1, ax2) = plt.subplots(2)
ax1.plot(df["Close"], color = "blue", label = "Closing Price")
ax1.plot(df["sar"], color = "red", label = "SAR")
ax2.plot(df["Close"], color = "blue", label = " Closing Price")
ax2.plot(df["up_trend"], color = "green", label = "up trend")
ax2.plot(df["down_trend"], color = "red" , label = "down trend")
date_format = mpl_dates.DateFormatter('%d %b %Y')
for ax in [ax1, ax2]:
	ax.legend(loc = "best")
	ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()
plt.show() 



print(df) 


fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5)
candlestick_ohlc(ax1,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)
ax1.plot(df["average"], label = "average")
ax1.plot(df['UpperBand'], label = "Upper Bollinger Band")
ax1.plot(df['LowerBand'], label = "Lower Bollinger Band")
ax2.plot(df["%K"], linestyle = "-", color = "blue", label = "%K")
ax2.plot(df["%D"], linestyle = "-", color = "orange", label = "%D")
ax2.axhline(80, linestyle='--', color = 'red')
ax2.axhline(20, linestyle='--', color = 'red')
ax3.plot(df["adx"], linestyle = "-", color = "blue", label = "ADX")
ax3.plot(df["plus_di"], linestyle = "-", color = "green", label = "+DI")
ax3.plot(df["minus_di"], linestyle = "-", color = "red", label = "-DI")
ax3.axhline(25, linestyle = "--", color = "black")
ax4.plot(df["rsi_14"], color = "orange", label = "rsi") 
ax4.axhline(50, linestyle = '--', linewidth = 1.5, color = 'blue')
ax5.plot(df['diff'], label = "bbw")
date_format = mpl_dates.DateFormatter('%d %b %Y')
for ax in [ax1, ax2, ax3, ax4, ax5]:
	#ax.legend(loc = "best")
	ax.xaxis.set_major_formatter(date_format)
	ax.legend(loc= "upper left")
fig.autofmt_xdate()
fig.legend(bbox_to_anchor=(1.3, 0.6))
#plt.savefig("t.png")
plt.show() 




import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-01",end="2021-06-29")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)
#print(df.shift(1))
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
#df = df.dropna()

print(df)
plt.rcParams["figure.figsize"] = [12, 7]
plt.rc('font', size=14)
fig, (ax1, ax2) = plt.subplots(2)
candlestick_ohlc(ax1,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8) 
ax2.plot(df["adx"], linestyle = "-", color = "blue", label = "ADX")
ax2.plot(df["plus_di"], linestyle = "-", color = "green", label = "+DI")
ax2.plot(df["minus_di"], linestyle = "-", color = "red", label = "-DI")
ax2.axhline(25, linestyle = "--", color = "black")
ax2.legend(loc = "best")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
plt.show()



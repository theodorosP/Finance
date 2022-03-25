import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-03-1",end="2021-07-02")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]







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



exp1 = df["Close"].ewm(span=12, adjust=False).mean()
exp2 = df["Close"].ewm(span=26, adjust=False).mean()
macd = exp1-exp2
exp3 = macd.ewm(span=9, adjust=False).mean()
df["MACD"] = macd
df["exp3"] = exp3


period = 20
multiplier = 2
df['UpperBand'] = df['Close'].rolling(period).mean() + df['Close'].rolling(period).std() * multiplier
df['LowerBand'] = df['Close'].rolling(period).mean() - df['Close'].rolling(period).std() * multiplier

df["average"] = df["Close"].rolling(period).mean()

df['14-high'] = df['High'].rolling(14).max()
df['14-low'] = df['Low'].rolling(14).min()
df['%K'] = (df['Close'] - df['14-low'])*100/(df['14-high'] - df['14-low'])
df['%D'] = df['%K'].rolling(3).mean()
df = df[19:]
print(df)
for col in df.columns:
    print(col)

print(df["MACD"])

plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
candlestick_ohlc(ax1,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8) 
ax1.plot(df["average"], label = "average")
ax1.plot(df['UpperBand'], label = "Upper Bollinger Band")
ax1.plot(df['LowerBand'], label = "Lower Bollinger Band") 
ax2.plot(df["%K"], linestyle = "-", color = "blue", label = "%K")
ax2.plot(df["%D"], linestyle = "-", color = "orange", label = "%D")
ax2.axhline(80, linestyle='--', color = 'red')
ax2.axhline(20, linestyle='--', color = 'red')
ax3.plot(df["rsi_14"], linestyle = "-", color = "blue", label = "rsi")
ax3.axhline(50, linestyle = "-", color = "yellow")
ax3.legend(loc = "upper left")
ax4.plot(df["MACD"], linestyle = "-", color = "red", label = "MACD")
ax4.plot(df["exp3"], linestyle = "-", color = "blue", label = "signnal")
ax4.legend(loc = "upper left")
#fix the date
date_format = mpl_dates.DateFormatter('%d %b %Y')
fig.autofmt_xdate() 
ax2.legend(loc = "upper left")
plt.show()


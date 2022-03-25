import pandas as pd
import numpy as np
import yfinance
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval = "1d", start = "2021-04-01", end = "2021-06-25")
df["Date"] = pd.to_datetime(df.index)
df["Date"] = df["Date"].apply(mpl_dates.date2num)
#move date in the front and through the other values
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)

df_ha = df.copy()
for i in range(df_ha.shape[0]):
	if i > 0:
		df_ha.loc[df_ha.index[i],'Open'] = (df['Open'][i-1] + df['Close'][i-1])/2
	df_ha.loc[df_ha.index[i],'Close'] = (df['Open'][i] + df['Close'][i] + df['Low'][i] +  df['High'][i])/4
df_ha = df_ha.iloc[1:,:]



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

#df = df.loc[:,["Date", "Open", "High", "Low", "Close", "Volume", "rsi_14"]]


print(df)


fig , (ax1, ax2)= plt.subplots(2)
fig.suptitle("Heikin_Ashi \n rsi")




candlestick_ohlc(ax1, df_ha.values,width=0.6, colorup='green', colordown='red', alpha=0.8)
ax2.plot(df["rsi_14"])
ax2.axhline(50, linestyle='--', color='blue')
#fix the date
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 





plt.legend()
plt.show()


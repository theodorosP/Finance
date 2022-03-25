import pandas as pd
import numpy as np
import yfinance
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval = "1d", start = "2021-03-01", end = "2021-07-12")
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







fig , (ax1, ax2)= plt.subplots(2)
fig.suptitle("Real values \n Candles")



candlestick_ohlc(ax1, df.values,width=0.6, colorup='green', colordown='red', alpha=0.8)
candlestick_ohlc(ax2, df_ha.values,width=0.6, colorup='green', colordown='red', alpha=0.8)

#fix the date
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 


fig.text(0.5, 0.03, "Dates", ha="center")
fig.text(0.04, 0.3, "Heikin_Ashi", va = "bottom", rotation = "vertical")
fig.text(0.02, 0.6, "Actual \n Candles", va = "bottom", rotation = "vertical")


plt.legend()
plt.show()









import yfinance
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-01",end="2021-06-28")
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]


print(df)


#print(df.iloc[:,4])
df["Typ Price"]  = (df["High"] + df["Low"] + df["Close"]) / 3 


l_mad = []
for i in range(0, len(df)):
	 l_mad.append( df["Typ Price"][i - 20:i].mad())

df["MAD"] = l_mad

l_sma = []
for i in range(0, len(df)):
	l_sma.append( df["Typ Price"][i - 20:i].mean())
df["SMA_Typ_Pr"] = l_sma


const = 0.015
df = df.iloc[20:]
print(df)
df["cci"] = (df["Typ Price"] - df["SMA_Typ_Pr"] ) / (const * df["MAD"]) 
print(df)



def get_signal(data, high, low):
	buy_signal = []
	sell_signal = []
	for i in range(len(data['cci'])):
		if data['cci'][i] > high:
			buy_signal.append(np.nan)
			sell_signal.append(data['Close'][i])
		elif data["cci"][i] < low:
			buy_signal.append(data['Close'][i])
			sell_signal.append(np.nan)
		else:
			sell_signal.append(np.nan)
			buy_signal.append(np.nan)

	return (buy_signal, sell_signal)

df['Buy'] = get_signal(df, 250, -250)[0]
df['Sell'] = get_signal(df, 250, -250)[1]
for i in range (0, len(df)):
	print (df["Buy"][i])


plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)
fig, (ax1, ax2) = plt.subplots(2)
candlestick_ohlc(ax1,df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8) 
ax1.scatter(df.index, df['Buy'], color='green', label='Buy Signal', marker='^', alpha = 1)
ax1.scatter(df.index, df['Sell'], color='red',  label='Sell Signal', marker='v', alpha = 1)
ax2.plot(df["cci"], linestyle = "-", color = "blue", label = "CCI")
ax2.axhline(250, linestyle = "-", color = "red")
ax2.axhline(-250, linestyle = "-", color = "red")
ax2.legend(loc = "best")
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
plt.show()


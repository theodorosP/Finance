import pandas as pd
import numpy as np
import yfinance
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)

name = 'DOGE-USD'
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-01", end="2021-06-23", index_col = "Date")
#first = df[["Open", "High", "Low", "Close"]]

df['Date'] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
print(df)

df_ha = df.copy()
for i in range(df_ha.shape[0]):
	if i > 0:
		df_ha.loc[df_ha.index[i],'Open'] = (df['Open'][i-1] + df['Close'][i-1])/2
	df_ha.loc[df_ha.index[i],'Close'] = (df['Open'][i] + df['Close'][i] + df['Low'][i] +  df['High'][i])/4
df_ha = df_ha.iloc[1:,:]

print(df_ha)


def isSupport(df,i):
	support = df_ha['Low'][i] < df_ha['Low'][i-1]  and df_ha['Low'][i] < df_ha['Low'][i+1] and df_ha['Low'][i+1] < df_ha['Low'][i+2] and df['Low'][i-1] < 		df['Low'][i-2]  
	return support
  
def isResistance(df,i):
	resistance = df_ha['High'][i] > df_ha['High'][i-1]  and df_ha['High'][i] > df_ha['High'][i+1] and df_ha['High'][i+1] > df_ha['High'][i+2] and 		df_ha['High'][i-1] > df_ha['High'][i-2]  
	return resistance
	
levels = []
for i in range(2,df_ha.shape[0]-2):
	if isSupport(df_ha,i):
		levels.append((i,df_ha['Low'][i]))
	elif isResistance(df_ha,i):
		levels.append((i,df_ha['High'][i]))


fig, ax = plt.subplots()  
candlestick_ohlc(ax,df_ha.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
fig.tight_layout() 
for level in levels:
	plt.hlines(y = level[1],xmin=df['Date'][level[0]],
	xmax=max(df['Date']),colors='blue')
plt.show()


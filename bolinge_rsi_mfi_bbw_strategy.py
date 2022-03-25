import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime
import numpy as np

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-03-24",end="2021-07-12")
#print(df.index)
#make index column
df["Date"] = pd.to_datetime(df.index)
df['Date'] = df['Date'].apply(mpl_dates.date2num)
#use all rows and the mentioned columns
df1 = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
df1 = df1[20:]


df_ha = df.copy()
for i in range(df_ha.shape[0]):
	if i > 0:
		df_ha.loc[df_ha.index[i],'Open'] = (df['Open'][i-1] + df['Close'][i-1])/2
	df_ha.loc[df_ha.index[i],'Close'] = (df['Open'][i] + df['Close'][i] + df['Low'][i] +  df['High'][i])/4
df_ha = df_ha.iloc[1:,:]

df_ha = df_ha.loc[:,['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]


period = 20
multiplier = 2
df_ha['UpperBand'] = df['Close'].rolling(period).mean() + df['Close'].rolling(period).std() * multiplier
df_ha['LowerBand'] = df['Close'].rolling(period).mean() - df['Close'].rolling(period).std() * multiplier

df_ha["average"] = df["Close"].rolling(period).mean()



typical_price = (df['Close'] + df['High'] + df['Low']) / 3


period =  14 #The typical period used for MFI is 14 days

money_flow = typical_price * df['Volume']


positive_flow =[] #Create a empty list called positive flow
negative_flow = [] #Create a empty list called negative flow
#Loop through the typical price 
for i in range(1, len(typical_price)):
	if typical_price[i] > typical_price[i-1]: #if the present typical price is greater than yesterdays typical price
		positive_flow.append(money_flow[i-1])# Then append money flow at position i-1 to the positive flow list
		negative_flow.append(0) #Append 0 to the negative flow list
	elif typical_price[i] < typical_price[i-1]:#if the present typical price is less than yesterdays typical price
		negative_flow.append(money_flow[i-1])# Then append money flow at position i-1 to negative flow list
		positive_flow.append(0)#Append 0 to the positive flow list
	else: #Append 0 if the present typical price is equal to yesterdays typical price
		positive_flow.append(0)
		negative_flow.append(0)


positive_mf =[]
negative_mf = [] 
#Get all of the positive money flows within the time period
for i in range(period-1, len(positive_flow)):
	positive_mf.append(sum(positive_flow[i+1-period : i+1]))
#Get all of the negative money flows within the time period  
for i in range(period-1, len(negative_flow)):
	negative_mf.append(sum(negative_flow[i+1-period : i+1]))



mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf)  + np.array(negative_mf) ))
print(len(mfi))



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



print(len(df_ha))
df2 =df[14:]
df2["mfi"] = mfi
print(df2)


df_ha['rsi_14'] = get_rsi(df['Close'], 14)
#df_ha["mfi"] = mfi
#df = df.dropna()
df_ha = df_ha.loc[:,["Date", "Open", "High", "Low", "Close", "Volume", "rsi_14", "UpperBand","LowerBand", "average"]]




limited_df = df_ha.copy()
print(limited_df)


period  =20
df = df[20:]
#print(df)
limited_df = df_ha[period -1:]
limited_df["rsi"] = df_ha["rsi_14"]
limited_df["diff"] = limited_df["UpperBand"] - limited_df["LowerBand"]
print(limited_df)

df2 = df2[(len(df2) - len(limited_df)) : ]
print(df2)
limited_df["mfi"] = df2["mfi"]
print(limited_df)

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
limited_df['Buy'] = get_signal(limited_df, 70, 30)[0]
limited_df['Sell'] = get_signal(limited_df, 70, 30)[1]


#print(limited_df.dropna(subset=['Buy']))




plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)

fig, ax = plt.subplots()  
candlestick_ohlc(ax,limited_df.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
fig.tight_layout() 

plt.plot(limited_df["average"], label = "average")
plt.plot(limited_df['UpperBand'], label = "Upper Bollinger Band")
plt.plot(limited_df['LowerBand'], label = "Lower Bollinger Band")

plt.legend()

plt.show()

fig , (ax1, ax2, ax4, ax5)= plt.subplots(4)

fig.suptitle("Bolinger Bands \n RSI")
candlestick_ohlc(ax1,df1.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
ax1.plot(limited_df["average"], label = "average")
ax1.plot(limited_df['UpperBand'], label = "Upper Bollinger Band")
ax1.plot(limited_df['LowerBand'], label = "Lower Bollinger Band")
ax1.scatter(limited_df.index, limited_df['Buy'], color='green', label='Buy Signal', marker='^', alpha = 1)
ax1.scatter(limited_df.index, limited_df['Sell'], color='red',  label='Sell Signal', marker='v', alpha = 1)
ax2.plot(limited_df["rsi"], label = "rsi")
ax2.axhline(50, linestyle='--', color = 'orange')
ax2.axhline(70, linestyle='--', color = 'red')
ax2.axhline(30, linestyle='--', color = 'red')
ax4.plot(limited_df["mfi"], label = "mfi")
ax4.axhline(50, linestyle='--', color = 'red')
#candlestick_ohlc(ax3,limited_df.values,width=0.6, \
#colorup='green', colordown='red', alpha=0.8)
ax5.plot(limited_df["diff"], linestyle = "-", color = "grey", label = "BBW")


#fix the date
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
#ax3.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
for i in [ ax2 ,ax4, ax5]:
	i.legend()
fig.text(0.5, 0.03, "Dates", ha="center")
fig.text(0.04, 0.5, "Doge Coin", va = "center", rotation = "vertical")
plt.show()


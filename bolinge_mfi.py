import yfinance
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
import datetime
import numpy as np

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-1",end="2021-07-12")
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


df2 = df1.tail(df1.shape[0] - period)


typical_price = (df['Close'] + df['High'] + df['Low']) / 3


period =  14 #The typical period used for MFI is 14 days

money_flow = typical_price * df['Volume']
print(money_flow)

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

print(len(positive_flow))

positive_mf =[]
negative_mf = [] 
#Get all of the positive money flows within the time period
for i in range(period-1, len(positive_flow)):
	positive_mf.append(sum(positive_flow[i+1-period : i+1]))
#Get all of the negative money flows within the time period  
for i in range(period-1, len(negative_flow)):
	negative_mf.append(sum(negative_flow[i+1-period : i+1]))



mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf)  + np.array(negative_mf) ))
print(mfi)


#Create a new data frame
new_df = pd.DataFrame()
new_df = df[period:]
new_df['MFI'] = mfi





plt.rcParams['figure.figsize'] = [12, 7]

plt.rc('font', size=14)

fig, ax = plt.subplots()  
candlestick_ohlc(ax,df2.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
fig.tight_layout() 

plt.plot(df["average"], label = "average")
plt.plot(df['UpperBand'], label = "Upper Bollinger Band")
plt.plot(df['LowerBand'], label = "Lower Bollinger Band")

plt.legend()

plt.show()









fig , (ax1, ax2)= plt.subplots(2)
fig.suptitle("Bolinger Bands \n MFI")



candlestick_ohlc(ax1,df2.values,width=0.6, \
colorup='green', colordown='red', alpha=0.8)  
#date_format = mpl_dates.DateFormatter('%d %b %Y')
#ax.xaxis.set_major_formatter(date_format)
#fig.autofmt_xdate() 
#fig.tight_layout() 

ax1.plot(df["average"], label = "average")
ax1.plot(df['UpperBand'], label = "Upper Bollinger Band")
ax1.plot(df['LowerBand'], label = "Lower Bollinger Band")

plt.legend(loc = "best")


ax2.plot(new_df["MFI"])
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






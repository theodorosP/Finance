import numpy as np
import yfinance
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-1",end="2021-06-24")

#print(df.columns)

#Copy date to another column named Data
df['Date'] = pd.to_datetime(df.index)
#Convert day to numbers
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]


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
print(mfi)



#Create a new data frame
limited_df = pd.DataFrame()
limited_df = df[period:]
limited_df['MFI'] = mfi
# Print the limited data frame for debugging
#print(limited_df)

# Automate the buy and sell signals
def get_signal(data, high, low):
	buy_signal = []
	sell_signal = []
	for i in range(len(data['MFI'])):
		if data['MFI'][i] > high:
			buy_signal.append(np.nan)
			sell_signal.append(data['Close'][i])
		elif data['MFI'][i] < low:
			buy_signal.append(data['Close'][i])
			sell_signal.append(np.nan)
		else:
			sell_signal.append(np.nan)
			buy_signal.append(np.nan)

	return (buy_signal, sell_signal)
# Add new columns for Buy and Sell
limited_df['Buy'] = get_signal(limited_df, 80, 20)[0]
limited_df['Sell'] = get_signal(limited_df, 80, 20)[1]
# Show the data
print(limited_df)

df2 = pd.DataFrame()
df2 = df[period:]
df2['MFI'] = mfi

plt.figure(figsize=(12.2, 4.5))
plt.plot(df['Close'], label = 'Close Price', alpha = 0.5)
plt.scatter(limited_df.index, limited_df['Buy'], color='green', label='Buy Signal', marker='^', alpha = 1)
plt.scatter(limited_df.index, limited_df['Sell'], color='red', label='Sell Signal', marker='v', alpha = 1)
plt.title('Close Price')
plt.xlabel('Date')
plt.ylabel('Close Price USD ($)')
plt.legend(loc='upper left')
plt.show()
# Create a plot
plt.figure(figsize=(12.2, 4.5))
plt.plot(df2['MFI'], label = 'MFI')
plt.axhline(10, linestyle='--', color='orange')
plt.axhline(20, linestyle='--', color='blue')
plt.axhline(80, linestyle='--', color='blue')
plt.axhline(90, linestyle='--', color='orange')
plt.title('MFI')
plt.ylabel('MFI Values')
plt.show()








fig , (ax1, ax2)= plt.subplots(2)
fig.suptitle("Real values \n MFI")



ax1.plot(df['Close'], label = 'Close Price', alpha = 0.5)
ax1.scatter(limited_df.index, limited_df['Buy'], color='green', label='Buy Signal', marker='^', alpha = 1)
ax1.scatter(limited_df.index, limited_df['Sell'], color='red', label='Sell Signal', marker='v', alpha = 1)




ax2.plot(df2['MFI'], label = 'MFI')
ax2.axhline(10, linestyle='--', color='orange')
ax2.axhline(20, linestyle='--', color='blue')
ax2.axhline(50, linestyle='--', color='blue')
ax2.axhline(80, linestyle='--', color='blue')
ax2.axhline(90, linestyle='--', color='orange')

#fix the date
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax1.xaxis.set_major_formatter(date_format)
ax2.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 


fig.text(0.5, 0.03, "Dates", ha="center")
fig.text(0.04, 0.5, "Doge Coin", va = "center", rotation = "vertical")



for ax in [ax1]:
        ax.legend(loc = "best")
        ax.label_outer()


plt.legend()
plt.show()

import numpy as np
import yfinance
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import datetime

name = "DOGE-USD"
ticker = yfinance.Ticker(name)
df = ticker.history(interval="1d",start="2021-04-1",end="2021-07-21")

#print(df.columns)

#Copy date to another column named Data
df['Date'] = pd.to_datetime(df.index)
#Convert day to numbers
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
print (df)

typical_price = (df['Close'] + df['High'] + df['Low']) / 3
print(typical_price)

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
print(new_df)
'''
#Show the new data frame
plt.plot(new_df["MFI"])
plt.show()
'''

fig, ax = plt.subplots()  
plt.plot(new_df["MFI"])
plt.axhline(50, linestyle='--', color = 'orange')
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate() 
fig.tight_layout()
plt.show()
	
	
	
	

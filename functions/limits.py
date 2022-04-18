import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
from datetime import datetime
import os




loc = "/home/thodoris/Desktop/Finance/folder/"

def isSupport(df,i):
	support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < 		df['Low'][i-2]  
	return support
  
def isResistance(df,i):
	resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and 		df['High'][i-1] > df['High'][i-2]  
	return resistance

def get_data(name):
    print("Data for " + str(name) + " download. Please hold.")
    ticker = yfinance.Ticker(name)
    df = ticker.history(interval="1d",start="2021-10-1",end=datetime.today().strftime('%Y-%m-%d'))
    df["Date"] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
    return df

def get_limit(name):
    df = get_data(name)
    levels = []
    for i in range(2,df.shape[0]-2):
	    if isSupport(df,i):
		    levels.append((i,df['Low'][i]))
	    elif isResistance(df,i):
		    levels.append((i,df['High'][i]))
    os.chdir(loc + str(name))
    plt.rcParams['figure.figsize'] = [12, 7]
    plt.rc('font', size=14)
    fig, ax = plt.subplots()  
    candlestick_ohlc(ax,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8)  
    date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate() 
    fig.tight_layout() 
    for level in levels:
	    plt.hlines(y = level[1],xmin=df['Date'][level[0]], xmax=max(df['Date']),colors='blue')
    #plt.savefig("sdf.png")
    plt.savefig("limits_" + str(name) + ".png")


l = [ "BTC-USD", "BCH-USD", "BSV-USD", "DOGE-USD", "ETH-USD", "ETC-USD", "LTC-USD", "SHIB-USD", "MATIC-USD", "SOL-USD"]
for i in l:
    get_limit(i)

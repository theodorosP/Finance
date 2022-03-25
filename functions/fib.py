import yfinance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
from datetime import datetime
import os

loc = "/home/thodoris/Desktop/Finance/folder/"

def get_data(name):
    print("Data for " + str(name) + " download. Please hold.")
    ticker = yfinance.Ticker(name)
    df = ticker.history(interval="1d",start="2022-03-8",end=datetime.today().strftime('%Y-%m-%d'))
    df["Date"] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
    return df

def fib(name):
    df = get_data(name)
    #Copy date to another column named Data
    df['Date'] = pd.to_datetime(df.index)
    #Convert day to numbers
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]


    highest_swing = -1
    lowest_swing = -1

    for i in range(1,df.shape[0]-1):
	    if df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i+1] and (highest_swing == -1 or df['High'][i] > df['High'][highest_swing]):
		        highest_swing = i
	    if df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i+1] and (lowest_swing == -1 or df['Low'][i] < df['Low'][lowest_swing]):
    	    	    lowest_swing = i		    


    ratios_up = [0, 0.236, 0.382, 0.5 , 0.618, 0.786, 1]

    ratios_down = [ 1 , 0.764, 0.618, 0.5, 0.382, 0.236, 0]
    colors = ["black","r","g","b","cyan","magenta","yellow"]
    levels_up = []
    levels_down = []

    max_level = df['High'][highest_swing]
    min_level = df['Low'][lowest_swing]
    

    if highest_swing > lowest_swing: # Uptrend
	    for ratio in ratios_up:
		    levels_up.append(max_level - (max_level-min_level)*ratio)
    else:
	    for ratio in ratios_down:
		    levels_down.append(min_level + (max_level-min_level)*ratio)


		

    plt.rcParams['figure.figsize'] = [12, 7]
    plt.rc('font', size=14)


    os.chdir(loc + str(name))
    fig, ax = plt.subplots()  
    candlestick_ohlc(ax,df.values,width=0.6, \
    colorup='green', colordown='red', alpha=0.8)  
    date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate() 
    fig.tight_layout() 


    for i in range(0, max(len(levels_up), len(levels_down))):
	    if len(levels_down) == 0:
		    plt.hlines(levels_up[i],df["Date"].min(), df["Date"].max(),label="{:.1f}%".format(ratios_up[i]*100),colors=colors[i], linestyles="dashed")
	    elif len(levels_up) == 0:
		    plt.hlines(levels_down[i],df["Date"].min(), df["Date"].max(),label="{:.1f}%".format(ratios_down[i]*100),colors=colors[i], linestyles="dashed")


    plt.legend(loc = "best")
    plt.savefig("fibb_"+str(name) + ".png")


l = [ "BTC-USD", "BCH-USD", "BSV-USD", "DOGE-USD", "ETH-USD", "ETC-USD", "LTC-USD"]
for i in l:
    fib(i)

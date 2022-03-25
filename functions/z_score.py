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
    df = ticker.history(interval="1d",start="2021-10-1",end=datetime.today().strftime('%Y-%m-%d'))
    df["Date"] = pd.to_datetime(df.index)
    df['Date'] = df['Date'].apply(mpl_dates.date2num)
    df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]
    return df

def get_z_score(name):
    df = get_data(name)
    period = 21
    df["average"] = df["Close"].rolling(period).mean()
    df["std"] = df["Close"].rolling(period).std()
    df = df[period-1:]
    df["z"] = (df["Close"] - df["average"])/df["std"]

    os.chdir(loc + str(name))
    plt.rcParams["figure.figsize"] = [12, 7]
    plt.rc("font", size = 14)
    fig, (ax1, ax2) = plt.subplots(2)
    candlestick_ohlc(ax1,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8) 
    ax2.plot(df["z"], color = "blue", label ="Z")
    ax2.legend(loc = "best")
    date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax1.xaxis.set_major_formatter(date_format)
    ax2.xaxis.set_major_formatter(date_format)
    plt.axhline(y = 2, color = "red")
    plt.axhline(y = -2, color = "red")
    fig.autofmt_xdate() 
    plt.savefig("z_score_"+str(name) + ".png")

l = [ "BTC-USD", "BCH-USD", "BSV-USD", "DOGE-USD", "ETH-USD", "ETC-USD", "LTC-USD"]
for i in l:
    get_z_score(i)

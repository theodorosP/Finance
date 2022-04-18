from this import d
import yfinance
import talib
import pandas as pd
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

def get_cci(name):
    df = get_data(name)
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
    df["cci"] = (df["Typ Price"] - df["SMA_Typ_Pr"] ) / (const * df["MAD"]) 


    #SAR
    sar = talib.SAR(df['High'], df['Low'], 0.02)
    df["sar"] = sar

    os.chdir(loc + str(name))
    plt.rcParams['figure.figsize'] = [12, 7]
    plt.rc('font', size=14)
    fig, (ax1, ax2, ax3) = plt.subplots(3)
    candlestick_ohlc(ax1,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8) 
    ax2.plot(df["cci"], linestyle = "-", color = "blue", label = "CCI")
    ax2.axhline(250, linestyle = "-", color = "red")
    ax2.axhline(-250, linestyle = "-", color = "red")
    candlestick_ohlc(ax3,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8) 
    ax3.plot( df["sar"], color = "blue", label = "SAR")
    ax2.legend(loc = "best")
    date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax1.xaxis.set_major_formatter(date_format)
    ax2.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate() 
    plt.savefig("cci_SAR_" + str(name) + ".png")

l = [ "BTC-USD", "BCH-USD", "BSV-USD", "DOGE-USD", "ETH-USD", "ETC-USD", "LTC-USD", "SHIB-USD", "MATIC-USD", "SOL-USD"]
for i in l:
    get_cci(i)

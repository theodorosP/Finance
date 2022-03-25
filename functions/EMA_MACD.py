import yfinance
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
    
def get_MACD_ema(name):
    print("Data for EMA and MACD are beeing downloaded, please wait..." + str(name))
    df = get_data(name)

    print(str(name) + " MACD")
    exp1 = df["Close"].ewm(span=12, adjust=False).mean()
    exp2 = df["Close"].ewm(span=26, adjust=False).mean()
    macd = exp1-exp2
    exp3 = macd.ewm(span=9, adjust=False).mean()
    df["MACD"] = macd
    df["exp3"] = exp3
    
    print(str(name) + " EMA")
    df['ema12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['ema26'] = df['Close'].ewm(span=26, adjust=False).mean()

    os.chdir(loc + str(name))
    print(str(name) + " Plot data")
    plt.rcParams["figure.figsize"] = [12, 7]
    plt.rc('font', size=14)
    fig, (ax1, ax2) = plt.subplots(2)
    candlestick_ohlc(ax1,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8) 
    ax1.plot(df["ema12"], linestyle = "-", color = "blue", label = "ema12")
    ax1.plot(df["ema26"], linestyle = "-", color = "red", label = "ema26")
    ax2.plot(df["MACD"], linestyle = "-", color = "blue", label = "MACD")
    ax2.plot(df["exp3"], linestyle = "-", color = "red")
    for ax in [ax1, ax2]:
        ax.legend(loc = "best")
    date_format = mpl_dates.DateFormatter('%d %b %Y')
    ax2.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate() 
    plt.savefig("ema_MACD_" + str(name) + ".png")

l = [ "BTC-USD", "BCH-USD", "BSV-USD", "DOGE-USD", "ETH-USD", "ETC-USD", "LTC-USD"]
for i in l:
	get_MACD_ema(i)

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

def get_adx(high, low, close, lookback):
	plus_dm = high.diff()
	minus_dm = low.diff()
	plus_dm[plus_dm < 0] = 0
	minus_dm[minus_dm > 0] = 0
	tr1 = pd.DataFrame(high - low)
	tr2 = pd.DataFrame(abs(high - close.shift(1)))
	tr3 = pd.DataFrame(abs(low - close.shift(1)))
	frames = [tr1, tr2, tr3]
	tr = pd.concat(frames, axis = 1, join = 'inner').max(axis = 1)
	atr = tr.rolling(lookback).mean()
	plus_di = 100 * (plus_dm.ewm(alpha = 1/lookback).mean() / atr)
	minus_di = abs(100 * (minus_dm.ewm(alpha = 1/lookback).mean() / atr))
	dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
	adx = ((dx.shift(1) * (lookback - 1)) + dx) / lookback
	adx_smooth = adx.ewm(alpha = 1/lookback).mean()
	return plus_di, minus_di, adx_smooth


def get_bb_rsi_stochastic_ADX_(name):
    print("Data for rsi, bb and Stochastic are beeing downloaded, please wait..." + str(name))
    df = get_data(name)
    print("ADX " + str(name))
    df['plus_di'] = get_adx(df['High'], df['Low'], df['Close'], 14)[0]
    df['minus_di'] = get_adx(df['High'], df['Low'], df['Close'], 14)[1]
    df['adx'] = get_adx(df['High'], df['Low'], df['Close'], 14)[2]
    df['rsi_14'] = get_rsi(df['Close'], 14)

    print(str(name) + " Stochastic is alculated")
    period = 20
    multiplier = 2
    df['UpperBand'] = df['Close'].rolling(period).mean() + df['Close'].rolling(period).std() * multiplier
    df['LowerBand'] = df['Close'].rolling(period).mean() - df['Close'].rolling(period).std() * multiplier
    df["average"] = df["Close"].rolling(period).mean()
    df['14-high'] = df['High'].rolling(14).max()
    df['14-low'] = df['Low'].rolling(14).min()
    df['%K'] = (df['Close'] - df['14-low'])*100/(df['14-high'] - df['14-low'])
    df['%D'] = df['%K'].rolling(3).mean()
    df = df[19:]

    print(str(name) + " Plot data")
    os.chdir(loc + str(name))
    plt.rcParams['figure.figsize'] = [12, 7]
    plt.rc('font', size=14)
    fig, (ax1) = plt.subplots()
    candlestick_ohlc(ax1,df.values,width=0.6, \
    colorup='green', colordown='red', alpha=0.8) 
    ax1.plot(df["average"], label = "average")
    ax1.plot(df['UpperBand'], label = "Upper Bollinger Band")
    ax1.plot(df['LowerBand'], label = "Lower Bollinger Band") 
    date_format = mpl_dates.DateFormatter('%d %b %Y')
    fig.autofmt_xdate() 
    plt.savefig(str(name) + ".png")
    

    df["bbw"] = df['UpperBand'] - df['LowerBand']
    plt.rcParams['figure.figsize'] = [12, 7]
    plt.rc('font', size=14)
    fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5)
    candlestick_ohlc(ax1,df.values,width=0.6, \
    colorup='green', colordown='red', alpha=0.8) 
    ax1.plot(df["average"], label = "average")
    ax1.plot(df['UpperBand'], label = "Upper Bollinger Band")
    ax1.plot(df['LowerBand'], label = "Lower Bollinger Band") 
    ax2.plot(df["rsi_14"], linestyle = "-", color = "blue", label = "rsi")
    ax2.axhline(50, linestyle = "--", color = "black")
    ax2.axhline(25, linestyle = "--", color = "red")
    ax2.axhline(75, linestyle = "--", color = "red")
    candlestick_ohlc(ax3,df.values,width=0.6, colorup='green', colordown='red', alpha=0.8) 
    ax3.plot(df["adx"], linestyle = "-", color = "blue", label = "ADX")
    ax3.plot(df["plus_di"], linestyle = "-", color = "green", label = "+DI")
    ax3.plot(df["minus_di"], linestyle = "-", color = "red", label = "-DI")
    ax3.axhline(25, linestyle = "--", color = "black")
    ax4.plot(df["%K"], linestyle = "-", color = "blue", label = "%K")
    ax4.plot(df["%D"], linestyle = "-", color = "orange", label = "%D")
    ax4.axhline(80, linestyle='--', color = 'red')
    ax4.axhline(20, linestyle='--', color = 'red')
    ax5.plot(df["bbw"], label = "bolinger band width")
    for ax in [ax1, ax2, ax3, ax4, ax5]:
        ax.legend(loc = "upper left")
    #fix the date
    date_format = mpl_dates.DateFormatter('%d %b %Y')
    fig.autofmt_xdate() 
    plt.savefig("rsi_bb_stochastic_" + str(name) + ".png")


l = [ "BTC-USD", "BCH-USD", "BSV-USD", "DOGE-USD", "ETH-USD", "ETC-USD", "LTC-USD"]
for i in l:
    get_bb_rsi_stochastic_ADX_(i)
    

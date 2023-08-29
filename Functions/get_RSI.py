#This function get the RSI index
#dataframe is the data we have. "Close" price is required
def get_rsi(dataframe, lookback):
    ret = dataframe["Close"].diff()
    up =list()
    down_ = list()
    for i in range(len(ret)):
        if ret[i] < 0:
            up.append(0)
            down_.append(ret[i])
        else:
            up.append(ret[i])
            down_.append(0)
    down = [abs(i) for i in down_]
    dataframe["up"] = up
    dataframe["down"] = down
    up_ewm = dataframe["up"].ewm(com = lookback - 1, adjust = False).mean()
    down_ewm = dataframe["down"].ewm(com = lookback - 1, adjust = False).mean()
    rs = up_ewm/down_ewm
    rsi = 100 - (100 / (1 + rs))
    df["RSI"] = rsi
    return dataframe

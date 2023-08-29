#This function get the MACD as well as the signal
#dataframe is the data we have. "Close" price is required
def get_MACD(dataframe):
  dataframe['ema12'] = np.NAN
  dataframe['ema26'] = np.NAN
  dataframe['ema12'] = dataframe['Close'].ewm(span=12, adjust=False).mean()
  dataframe['ema26'] = dataframe['Close'].ewm(span=26, adjust=False).mean()
  macd = dataframe['ema12'] - dataframe['ema26']
  signal = macd.ewm(span=9, adjust=False).mean()
  dataframe["MACD"] = macd
  dataframe["MACD_SIGNAL"] = signal
  return dataframe


#This function get the Buy and sell signals using the MACD indicator
#dataframe is the data we have. "MACD"  and "MACD_SIGNAL" values are required
def get_MACD_signals(dataframe):
  signals = np.where(dataframe["MACD"] > dataframe["MACD_SIGNAL"], 1, -1)
  signals = np.where(dataframe["MACD"].isnull(), 0, signals)
  signals_list = [signals[0]]
  for i in range(1, len(signals)):
    if signals[i] == signals[i -1]:
      signals_list.append(0)
    else:
      signals_list.append(signals[i])
  dates_bought = list()
  dates_sold = list()
  dataframe["Buy"] = np.NAN
  dataframe["Sell"] = np.NAN
  for i in range(0, len(dataframe)):
    if signals_list[i] == 1:
      dates_bought.append(dataframe.index[i])
      dataframe["Buy"][i] = dataframe["Close"][i]
    elif signals_list[i] == -1:
      dates_sold.append(dataframe.index[i])
      dataframe["Sell"][i] = dataframe["Close"][i]
  return dataframe

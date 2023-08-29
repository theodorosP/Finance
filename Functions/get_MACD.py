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

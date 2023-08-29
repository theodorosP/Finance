#This function get the upper and lowwer bolinger band
#dataframe is the data we have. "Close" price is required
def get_bolinger_bands(dataframe):
  period = 20
  multiplier = 2
  dataframe['UpperBand'] = dataframe['Close'].rolling(period).mean() + dataframe['Close'].rolling(period).std() * multiplier
  dataframe['LowerBand'] = dataframe['Close'].rolling(period).mean() - dataframe['Close'].rolling(period).std() * multiplier
  return dataframe

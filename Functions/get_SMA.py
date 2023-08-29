#this codes gives the snimle moving average
#dataframe is the dataframe with our data.
#window is the lag. How many days we look back
#title is the name of column in the dataframe of the calculated quantity

def get_SMA(dataframe, window, title):
  N = len(dataframe)
  average_values = list()
  for i in range(window, N):
    average_values.append(np.mean(dataframe["Close"][i - window : i]))
  dataframe[title] = np.nan

  for i in range(window, N):
    dataframe[title][i] = average_values[i - window]
  return dataframe

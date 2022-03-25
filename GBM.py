import numpy as np
import matplotlib.pyplot as plt


mu = 0.001
sigma = 0.1
start_price = 5

np.random.seed(0)
returns = np.random.normal(loc=mu, scale=sigma, size=100)
price = start_price*(1+returns).cumprod()

plt.plot(price)
plt.show()

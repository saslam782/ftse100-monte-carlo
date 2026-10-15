# Monte Carlo simulation of the FTSE 100 - 1 year VaR and ES
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

# 5 years of daily closing prices
prices = yf.Ticker("^FTSE").history(start="2021-10-15", end="2026-10-15")["Close"]
prices.plot(title="FTSE 100")
plt.xlabel("Date")
plt.ylabel("Index level")
plt.show()

# daily log returns
returns = np.log(prices / prices.shift(1)).dropna()
mu = returns.mean()
sigma = returns.std()
print("Annual return:", round(mu * 252 * 100, 2), "%")
print("Annual volatility:", round(sigma * np.sqrt(252) * 100, 2), "%")

# simulate 10,000 one-year paths
S0 = prices.iloc[-1]
days = 252
sims = 10000
np.random.seed(42)
Z = np.random.standard_normal((days, sims))
paths = S0 * np.exp(np.cumsum(mu + sigma * Z, axis=0))

plt.plot(paths[:, :100])
plt.axhline(S0, color="black", linestyle="--")
plt.title("100 simulated paths")
plt.xlabel("Trading day")
plt.ylabel("Index level")
plt.show()

# results after 1 year
final = paths[-1]
final_returns = final / S0 - 1
print("Chance of a loss:", round((final < S0).mean() * 100, 1), "%")

var_95 = -np.percentile(final_returns, 5)
es_95 = -final_returns[final_returns <= -var_95].mean()
print("95% VaR:", round(var_95 * 100, 1), "%")
print("95% ES:", round(es_95 * 100, 1), "%")

plt.hist(final, bins=100)
plt.axvline(S0 * (1 - var_95), color="red", linestyle="--", label="95% VaR")
plt.title("FTSE 100 after 1 year (10,000 simulations)")
plt.xlabel("Index level")
plt.ylabel("Number of simulations")
plt.legend()
plt.show()










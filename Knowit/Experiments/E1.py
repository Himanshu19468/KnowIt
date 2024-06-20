import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fetch historical data
reliance = yf.download('RELIANCE.NS', start='2022-01-01', end='2023-12-31')['Close']
nifty = yf.download('^NSEI', start='2022-01-01', end='2023-12-31')['Close']

# Calculate Relative Strength (RS)
rs = reliance / nifty

# Calculate the momentum of RS (using a simple rate of change over a 5-day window for example)
rs_momentum = rs.pct_change(periods=5)

# Plot the RRG (RS on X-axis and RS Momentum on Y-axis)
plt.figure(figsize=(10, 6))
plt.scatter(rs, rs_momentum, color='blue', label='RELIANCE.NS')

# Plot the start and end points to visualize the movement
plt.scatter(rs.iloc[0], rs_momentum.iloc[0], color='green', label='Start')
plt.scatter(rs.iloc[-1], rs_momentum.iloc[-1], color='red', label='End')

# Annotate the start and end points
plt.text(rs.iloc[0], rs_momentum.iloc[0], 'Start', fontsize=10, va='bottom')
plt.text(rs.iloc[-1], rs_momentum.iloc[-1], 'End', fontsize=10, va='bottom')

plt.axhline(0, color='grey', lw=1)
plt.axvline(1, color='grey', lw=1)

plt.xlabel('Relative Strength (RS)')
plt.ylabel('RS Momentum')
plt.title('Relative Rotation Graph (RRG) compared to NIFTY 50')
plt.legend()
plt.grid(True)
plt.show()

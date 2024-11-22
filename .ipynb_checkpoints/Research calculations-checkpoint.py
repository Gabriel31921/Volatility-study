# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 18:24:03 2024

@author: gborr
"""
import numpy as np
import datetime
import matplotlib.pyplot as plt
import time
import json
import pandas as pd

from statsmodels.graphics.tsaplots import plot_acf
from scipy.stats import shapiro, normaltest

#IMPORT DATA
with open('historical_candles.json', 'r') as f:
    loaded_data = json.load(f)

Time = loaded_data['Time']
Open = loaded_data['Open']
High = loaded_data['High']
Low = loaded_data['Low']
Close = loaded_data['Close']

vol_factor = np.sqrt(365 * 24)

#STEP 2.1 CALCULATING VOLATILITY WINDOWS WITH NON-OVERLAPPING WINDOWS

window_size = 24 #3 days of low-volatility is what we are hunting for
rolling_vol = []

returns = [np.log(Close[i+1]/Close[i]) for i in range(len(Close)-1)]

rolling_vol = pd.Series(returns).rolling(window = 24).std()

#Plot returns and rolling volatility
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(returns, label="Returns")
plt.title("Returns")
plt.subplot(2, 1, 2)
plt.plot(rolling_vol, label="Rolling Volatility", color="orange")
plt.title("Rolling Volatility (24-hour)")
plt.legend()
plt.tight_layout()
plt.show()

#Plot autocorrelation of squared returns (proxy for volatility)
plot_acf(np.square(returns), lags=50, title="Autocorrelation of Squared Returns")
plt.show()

'''
for i in range(0, len(Close), window_size):
    window = Close[i : i + window_size]
    if len(window) == window_size:
        returns = [np.log(window[j + 1] / window[j]) for j in range(len(window) - 1)]
        vol = np.std(returns, ddof=1)
        rolling_vol.append(vol * vol_factor)

#STEP 2.2 CALCULATING VOLATILITY WINDOWS WITH OVERLAPPING WINDOWS

window_size = 160
rolling_vol = []

#Iterate through overlapping windows
for i in range(len(Close) - window_size + 1):  #Ensure the window doesn't exceed bounds
    window = Close[i:i + window_size]
    returns = [np.log(window[j + 1] / window[j]) for j in range(len(window) - 1)]
    vol = np.std(returns, ddof=1)
    rolling_vol.append(vol * vol_factor)

log_vol = []

for vol in rolling_vol:
    if vol != 0:
        log_vol.append(np.log(vol))
    else:
        log_vol.append(vol)


plt.hist(rolling_vol, bins=100)
plt.title('Distribution of Annualized Volatility')
plt.xlabel('Annualized Volatility')
plt.ylabel('Frequency')
plt.grid()
plt.show()

#Step 3: Analyze distribution
mean_vol = np.mean(rolling_vol)
std_vol = np.std(rolling_vol, ddof=1)
print(f"Mean Volatility: {mean_vol:.4f}")
print(f"Standard Deviation of Volatility: {std_vol:.4f}")


#Normality tests
shapiro_test = shapiro(rolling_vol)
dagostino_test = normaltest(rolling_vol)

print("Shapiro-Wilk Test:")
print(f"Statistic: {shapiro_test.statistic:.4f}, p-value: {shapiro_test.pvalue:.4f}")
print("D’Agostino and Pearson’s Test:")
print(f"Statistic: {dagostino_test.statistic:.4f}, p-value: {dagostino_test.pvalue:.4f}")
'''
















# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 18:21:45 2024

@author: gborr
"""

import requests
import datetime
import time
import json

# Global variables
endTime_0 = int(datetime.datetime(2019, 1, 1, 0, 0, 0).timestamp() * 1000)

n_of_requests = 200
interval = 60*1000 * 60 * 200  # 200 hours in miliseconds
pause_count = 0  # Control how many requests to the API without pause.

symbol = ['BTCUSDT']
granularity = ['1h']
endTimes = [endTime_0]
limit = [200]  # Max is 200.

Time, Open, High, Low, Close = [], [], [], [], []

for i in range(1, n_of_requests):
    endTimes.append(endTimes[-1] + interval)

# print(endTimes) #For checking

# STEP 1. GETTING THE DATA.

# Getting the historical candle info for a symbol
url = 'https://api.bitget.com/api/v2/spot/market/history-candles'

for endTime in endTimes:
    params = {
        'symbol': symbol[0],
        'granularity': granularity[0],
        'endTime': endTime,
        'limit': limit[0]
    }

    response = requests.get(url, params)

    initial_data = response.json()

    data = initial_data['data']

    for i in range(len(data)):
        Time.append(float(data[i][0]))
        Open.append(float(data[i][1]))
        High.append(float(data[i][2]))
        Low.append(float(data[i][3]))
        Close.append(float(data[i][4]))

    if pause_count == 15:  # Rate limit is 20/s, but just to be safe
        time.sleep(1)
        pause_count = 0
    else:
        pause_count += 1

data_dict = {
    'Time': Time,
    'Open': Open,
    'High': High,
    'Low': Low,
    'Close': Close
    }
    
# Save to a JSON file
with open('historical_candles.json', 'w') as f:
    json.dump(data_dict, f)
print("Data saved to 'historical_candles.json'")























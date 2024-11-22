import requests
import time
import datetime
import numpy as np
import websocket
import json
import threading


'''
#Getting the info for a symbol
url = "https://api.bitget.com/api/v2/spot/public/symbols"
params = {"symbol": "BTCUSDT"}  # Add any parameters here

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}", response.text)


endTime_0 = int(datetime.datetime(2024, 11, 14, 0, 0, 0).timestamp() * 1000)

#Getting the historical candle info for a symbol
url = 'https://api.bitget.com/api/v2/spot/market/history-candles'
params_0 = {
    'symbol'      : 'BTCUSDT',
    'granularity' : '1h',
    'endTime'     : endTime_0,
    'limit'       : '200'
}

endTime_1 = endTime_0 + 200*60*1000

params = {
    'symbol'      : 'BTCUSDT',
    'granularity' : '1h',
    'endTime'     : endTime_1,
    'limit'       : '200'
}

response_0 = requests.get(url, params = params)
response_1 = requests.get(url, params = params)

data_0 = response_0.json()
data_1 = response_1.json()

Final_data = data_0['data'] + data_1['data']

for i in range(len(Final_data)):
    Final_data[i] = [float(value) for value in Final_data[i]]

Time    = []
Open    = []
High    = []
Low     = []
Close   = []

for i in range(len(Final_data)):
    Time.append(Final_data[i][0])
    Open.append(Final_data[i][1])
    High.append(Final_data[i][2])
    Low.append(Final_data[i][3])
    Close.append(Final_data[i][4])


returns = []

for i in range(len(Close)):
    if i != max(range(len(Close))):
        returns.append(np.log(Close[i+1]/Close[i]))
         

#A better approach
returns = [np.log(Close[i + 1] / Close[i]) for i in range(len(Close) - 1)]
vol = np.std(returns, ddof= 1)
annual_vol = vol * np.sqrt(365*24)

#element_2 = datetime.datetime.fromtimestamp(ending_time_unix / 1000)
#print(element_2)
'''

#Debugging this hell of a program
received_first_message = False

#Global variables
window_size = 2000
start_time = time.time()
update_interval = 5 #Every how many seconds you get an update
stop_udate = 60 #How many seconds does the connection stay open

#Data variables
Time    = []
Open    = []
High    = []
Low     = []
Close   = []

websocket_public_url  = 'wss://ws.bitget.com/v2/ws/public'
websocket_private_url = 'wss://ws.bitget.com/v2/ws/private'
websocket_candle_params = {
    "op": "subscribe",
    'args' : [
        {
        'instType' : 'USDT-FUTURES',
        'channel' : 'candle1m',
        'instId'  : 'BTCUSDT'
        }        
        ]
    }

# Open connection
def on_open(ws):
    print("WebSocket connection opened")
    #Suscribing to somthg
    ws.send(json.dumps(websocket_candle_params))
    print('Sent subscription mssg:', websocket_candle_params)
    
# Close connection
def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed")

# Error handler
def on_error(ws, error):
    print("Error:", error)

# Interrupt handler
def stop_connection(ws):
    print("Closing connection...")
    ws.close()  # Gracefully close the WebSocket connection
    
def on_message(ws, message):
    global Time, Open, High, Low, Close, received_first_message
    
    parsed_message = json.loads(message)
    
    #I've been told to do this but...
    if 'data' in parsed_message and isinstance(parsed_message['data'], list):
        data = parsed_message['data'] #As for lines ZZZ to ZZZ, we know we are working with a list of lists.
        
        for item in data: #For each list in data (which is one btw)
        
            if item[0] in Time:
                idx = Time.index(item[0])
                Open[idx] = item[1]
                High[idx] = item[2]
                Low[idx]  = item[3]
                Close[idx] = item[4]
                
            else:
                Time.append(item[0])
                Open.append(item[1])
                High.append(item[2])
                Low.append(item[3])
                Close.append(item[4])

    #More debugging proof:
    print('Processed data:', Time[-1], Open[-1], High[-1], Low[-1], Close[-1])
 
#    if not received_first_message:
#        received_first_message = True
#        print('Stopping Websocket after first update (maybe)...')
#        ws.close() #Closing and praying

ws = websocket.WebSocketApp(
    websocket_public_url,
    on_open= on_open,
    on_message= on_message,
    on_error= on_error,
    on_close= on_close
    )

ws.run_forever()


'''
Message received: {
    "action":"update",
    "arg":               
        {"instType":"SPOT",
         "channel":"candle1H",
         "instId":"BTCUSDT"},
    "data":
        [["1731675600000",
          "89729.95",
          "89970.08",
          "89304.96",
          "89762.75",
          "105.913661",
          "9502924.99958111",
          "9502924.99958111"]],
    "ts":1731678136633}
'''





































    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

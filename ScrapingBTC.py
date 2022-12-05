import os
import cbpro
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import csv
from tabulate import tabulate
from dateutil import parser


api_url="https://api.pro.coinbase.com"
sym='BTC-USD'
barSize="3600" #sat vremena
timeEnd= datetime.now()

delta= timedelta(hours=1)

timeStart= timeEnd - (300*delta)

timeStart=timeStart.isoformat()
timeEnd=timeEnd.isoformat()
i=0
parameters={
    "start": timeStart,
    "end": timeEnd,
    "granularity": barSize
    }
#df_final = pd.DataFrame(columns=["time", "low", "high", "open", "close"]


while i<15:

    data = requests.get(f'{api_url}/products/{sym}/candles',
                            params={"start": timeStart,
                                    "end": timeEnd,
                                    "granularity": barSize}
                            ,headers={"content-type":"aplication/json"})
    #public_client= cbpro.PublicClient()
    #result=public_client.get_product_order_book('BTC-USD')
    df = pd.DataFrame(data.json(),
                          columns=["time", "low", "high", "open", "close", "volume"]
                          )
    df["time"] = pd.to_datetime(df["time"], unit='s')
    df = df[["time", "open", "high", "low", "close"]]  # mozemo i volume al ne treba nam
    #df.reset_index(drop=True, inplace=True)

    if i==0:
        df.to_csv('coinbase.csv', index=False)
    else:
        df.columns = df.iloc[0]
        df = df[1:]
        df.to_csv('coinbase.csv', mode='a', index=False)

    timeEnd = datetime.fromisoformat(timeStart)
    timeStart = timeEnd - (300 * delta)
    timeEnd=timeEnd.isoformat()
    timeStart=timeStart.isoformat()
    i=i+1

a = pd.read_csv("coinbase.csv")
b = pd.read_csv("coinbase1.csv")
c = pd.read_csv("coinbase2.csv")
#b = b.dropna(axis=1)
merged = pd.merge(a,b,left_on='time',right_on='time',how='left')
merged.columns = ['time', 'open_btc', 'high_btc', 'low_btc','close_btc'
                  ]
merged.to_csv("output.csv", index=False)

final = pd.merge(merged,c,left_on='time',right_on='time',how='left')
final.columns = ['time', 'open_btc', 'high_btc', 'low_btc','close_btc']
final.to_csv('final.csv', index=False)


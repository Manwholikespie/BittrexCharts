import json
from pprint import pprint
# ---
from coin import Coin
# ---
from bittrex.bittrex import Bittrex
API_V2_0 = 'v2.0'
import requests
# import numpy as np

print('1/5 - Reading secrets...')
AUTH = json.loads(open('secrets.json','r').read())

print('2/5 - Authenticating...')
my_bittrex = Bittrex(AUTH['key'], AUTH['secret'])

def get_btc_price():
    print('3/5 - Getting BTC price...')
    url = 'https://bittrex.com/api/v2.0/pub/currencies/GetBTCPrice'
    r = requests.get(url)
    data = json.loads(r.content)

    if not bool(data['result']):
        raise Exception('API request was not successful.')
    
    return data['result']['bpi']['USD']['rate_float']

BTC_PRICE = get_btc_price()

def get_bal():
    global BTC_PRICE

    # get data we will use in later calculations to find portfolio worth.
    print('4/5 - Getting balances...')
    bal = my_bittrex.get_balances()
    if not bal.get('success'):
        raise Exception('API request was not successful.')
    
    print('5/5 - Getting market summaries...')
    market_data = my_bittrex.get_market_summaries()
    if not market_data.get('success'):
        raise Exception('Error fetching market data.')
    
    # where we will be storing coin data before we make Coin objects.
    myCoins = {}

    # coins I'm invested in
    for c in bal['result']:
        if c['Available'] > 0.0:
            myCoins[c['Currency']] = {
                'balance' : c['Balance'],
                'ticker' : c['Currency']
            }
    
    # markets I'm invested in
    for market in market_data['result']:
        m = market['MarketName'].split('BTC-',1)[1:]

        if m:
            # current ticker
            if m[0] in myCoins:
                # If you wanted, you could change 'Bid' to 'Ask' or 'Last'
                myCoins[m[0]]['price'] = market['Bid']
    
    outputCoins = []

    # iterate over my coins, getting their market data.
    for coin in myCoins:
        if coin == 'BTC':
            outputCoins.append(Coin(
                ticker=coin,
                amount=myCoins[coin]['balance'],
                price=1, # 1 btc = 1 btc
                BTC_PRICE=BTC_PRICE
            ))
        else:
            outputCoins.append(Coin(
                ticker=coin,
                amount=myCoins[coin]['balance'],
                price=myCoins[coin]['price'],
                BTC_PRICE=BTC_PRICE
            ))
    
    return outputCoins
#!/usr/bin/env python

from bittrex import bittrex as B
import urllib.request
import json
from functools import reduce
from urllib.parse import quote
from coinmarketcap import Market as CMC
import sys
import pprint
from secrets import BKEY, BSECRET

account = B.Bittrex(BKEY,BSECRET)

BUY_ORDERBOOK = 'buy'
SELL_ORDERBOOK = 'sell'
BOTH_ORDERBOOK = 'both'
LOT = 5

CMC = CMC()


def find_invested_currencies():
    '''
    Find the currencies in Bittrex where balance > 0 
    rtype: list of dict
    '''
    invested = []
    for cur in account.get_balances()['result']:
        if cur['Balance'] > 0:
            invested.append({'currency': cur['Currency'],'Balance': cur['Balance']})
    return invested

def get_btc_lot_price_usd(qty=1):
    '''
    param qty: string
    this function takes in the dollar lot quantity and
    returns that as a BTC quantity
        ex:
            1 $5 LOT = .0023 btc
    rtype: float
    '''
    lot = LOT*qty
    req = urllib.request.Request("https://api.coinmarketcap.com/v1/ticker/bitcoin/")
    opener = urllib.request.build_opener()
    f = opener.open(req)
    jso = json.loads(f.read().decode('utf-8'))
    btc_usd = jso[0]['price_usd']
    btc_usd = float(btc_usd.encode('utf-8'))
    btcQty = (round(lot/btc_usd, 6))
    return btcQty

def get_currency_stats(cur_list):
    req = urllib.request.Request("https://api.coinmarketcap.com/v1/ticker/")
    opener = urllib.request.build_opener()
    f = opener.open(req)
    jso = json.loads(f.read().decode('utf-8'))
    total_bal = []
    for ci in cur_list:
        for cp in jso:
            if cp['symbol'] == ci['currency']:
                price_usd = float(cp['price_usd'].encode('utf-8'))
                cur_bal = float(ci['Balance'])
                usd_balance = price_usd * cur_bal
                total_bal.append(usd_balance)
                print(cp['name']+ ' $'+ str(usd_balance))
                coin_market = CMC.ticker(cp['id'])[0]
                print('Rank '+ coin_market['rank'],end=' | ')
                print('1HR %'+ coin_market['percent_change_1h'],end=' | ')
                print('24HR % '+ coin_market['percent_change_24h'],end=' | ')
                try:
                    print('7D %'+ coin_market['percent_change_7d'])
                except:
                    print('No Data')
                print("="*60)

    total_bal = reduce(lambda x, y: x+y, total_bal)
    total_bal = 'Balance $'+str(total_bal)
    return total_bal

def get_coin(coin_name):
    '''
    Use CMC to generate coin stats 
    param coin_name: string
    coin_name is full name ex: Bitcoin
    rtype dictionary
    '''
    coin_data = CMC.ticker(coin_name)
    coin_dict = {
        "Coin_Name": coin_data[0]["name"],
        "Ticker": coin_data[0]["symbol"],
        "USD_Price": coin_data[0]["price_usd"],
        "Bid": get_Bid(coin_data[0]["symbol"]),
        "Ask": get_Ask(coin_data[0]["symbol"]),
        "Percent_Change_7D": coin_data[0]["percent_change_7d"],
        "Percent_Change_1D": coin_data[0]["percent_change_24h"],
        "Percent_Change_24H": coin_data[0]["percent_change_1h"],
    }

    return coin_dict

def get_Ask(currency):
    '''
    Assumes BTC is the main market
    param currency: string
    currency is ticker ex: cvc
    currency cannot be BTC
    rtype: float
    '''
    currency = currency.upper()
    market = 'BTC-'+currency
    ask = account.get_market_summary(market)['result'][0]['Ask']
    return ask

def get_Bid(currency):
    '''
    Assumes BTC is the main market
    param currency: string
    currecny is ticker ex: cvc
    currency cannot be BTC
    rtype: float
    '''
    currency = currency.upper()
    market = 'BTC-'+currency
    bid = account.get_market_summary(market)['result'][0]['Bid']
    return bid


def get_Balance(currency):
    '''
    param currency: string
    rtype balance: float
    '''
    balance = account.get_balance(currency)
    return balance['result']['Balance']

def avail_BTC():
    '''
    Gets the maximum bitcoin AVAILABLE in account
    rtype: float
    '''
    print(account.get_balance('BTC')['result'])
    btc = account.get_balance('BTC')['result']['Available']
    return  btc

def buy_Cur(currency, lots=1, buyall=False, market_price=True):
    '''
    Assumes BTC is the main market and the amount is in US Dollars
    Min amount is 50,000 SAT
    param currency: string
    param lots (optional): int
    ***Buy All does not work yet!!!!!!!
    '''
    currency = currency.upper()
    market = 'BTC-{}'.format(currency)
    if not market_price:
        price = get_Bid(currency)
    else:
        price = get_Ask(currency)

    if buyall:
        qty = round(avail_BTC()/price, 5)
    else:
        qty = round(get_btc_lot_price_usd(lots)/price, 6)

    trade = account.buy_limit(market,qty, price)
    if trade['success']:
        print('Good Trade')
        print('UUID: ' + str(trade['result']['uuid']))
    else:
        print('trade not filled')
    return trade

def sell_Cur(currency, lots=1, sellall=False, market_price=True):
    '''
    Assumes BTC is the main market and the amount is in US Dollars
    Min amount is 50,000 SAT
    param currency: string
    param lots (optional): int
    '''
    currency = currency.upper()
    market = 'BTC-{}'.format(currency)
    if not market_price:
        price = get_Ask(currency)
    else:
        price = get_Bid(currency)
    if sellall:
        qty = get_Balance(currency)
    else:
        qty = round(get_btc_lot_price_usd(lots)/price, 6)
    trade = account.sell_limit(market, qty, price)
    if trade['success']:
        print('Good Trade')
        print('UUID: ' + str(trade['result']['uuid']))
    else:
        print('trade not filled')
    return trade

def get_open_orders(market):
    '''
    param market optional type string
    rtype dict
    '''
    return account.get_open_orders(market)

'''
    format: balance.py -b eth 10
'''


if len(sys.argv) == 1:

    bittrex_balance = find_invested_currencies()
    cur_stat = get_currency_stats(bittrex_balance)
    print(cur_stat)
    get_btc_lot_price_usd()

else:
    if sys.argv[1].startswith("-"):
        command = sys.argv[1].split('-')[1].upper()
        if command == 'B':
            if sys.argv[2]:
                currency = sys.argv[2].upper()
                if sys.argv[3]:
                    lots = float(sys.argv[3])
                    buy_Cur(currency, lots)
                else:
                    print('You must specify how many lots')
            else:
                print('You must specify currency pair')

        if command == 'S':
            if sys.argv[2]:
                currency = sys.argv[2].upper()
                if sys.argv[3]:
                    lots = float(sys.argv[3])
                    sell_Cur(currency, lots)
                else:
                    print('You must specify how many lots')
            else:
                print('You must specify currency pair')

        if command == 'SA':
            if sys.argv[2]:
                currency = sys.argv[2].upper()
                sell_Cur(currency,sellall=True)
            else:
                print('You must specify currency pair')

        if command == 'BA':
            if sys.argv[2]:
                currency = sys.argv[2].upper()
                buy_Cur(currency,buyall=True)
            else:
                print('You must specify currency pair')

        if command == 'N':
            if sys.argv[2]:
                coin_name = sys.argv[2].upper()
                coin_inf = get_coin(coin_name)
                for k in coin_inf.keys():
                    print(k,coin_inf[k])

        if command == 'BBID':
            if sys.argv[2]:
                currency = sys.argv[2].upper()
                buy_Cur(currency,market_price=False)
            else:
                print('You must specify a coin')

        if command == 'SASK':
            if sys.argv[2]:
                currency = sys.argv[2].upper()
                sell_Cur(currency,market_price=False)
            else:
                print('You must specify a coin')
        if command == 'OO':
            if sys.argv[2]:
                market = sys.argv[2].upper()
                print(get_open_orders(market))
            else:
                print("You must specifiy a market ex: BTC-ETH")
    else:
        print('commands start with single dash')


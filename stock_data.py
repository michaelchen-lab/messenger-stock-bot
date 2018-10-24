import os
import sys
import urllib.request
import json

def stock_match(msg):
    try:
        original = urllib.request.urlopen('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+msg+'&apikey=3VWEA280OOGR9AL4')
    except ValueError:
        print("\nInvalid Entry")
        start()
    data = json.load(original)

    best_match = [data['bestMatches'][0]['1. symbol'],data['bestMatches'][0]['9. matchScore']]
    return best_match

def get_data(sym,request_type):
    try:
        original = urllib.request.urlopen('https://api.iextrading.com/1.0/stock/'+sym+'/'+request_type)
    except ValueError:
        print("\nInvalid Entry")
        start()
    data = json.load(original)
    if request_type == 'chart/dynamic':
        data = data['data']
    return data

def stock_info(stock):
    data = get_data(stock,'book')
    info = [data['quote']['close'],data['quote']['latestTime']]
    return info
  

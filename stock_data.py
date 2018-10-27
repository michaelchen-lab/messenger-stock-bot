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

    ## Shows the most likely stock the user is searching for
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
    ## Returns the stock data requested by other functions
    return data

def stock_info(stock):
    data = get_data(stock,'book')
    data_company = get_data(stock,'company')
    website = data_company['website']

    ## Shows the stock's latest price, the time of quote, and website url
    info = [data['quote']['close'],data['quote']['latestTime'],website.replace('http://www.','')]
    return info

def stock_describe(stock):
    data = get_data(stock,'company')

    ## Shows the stock's name, CEO, sector, industry and description
    info = [data['companyName'],data['website'],'CEO',data['CEO'],'Sector',data['sector'],'Industry',data['industry'],'Description',data['description']]
    return info 
    

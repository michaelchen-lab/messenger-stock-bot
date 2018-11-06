import os
import sys
import urllib.request
import json

def stock_match(msg):
    ## Uses the API's search feature to return the most likely stock the user is searching for
    
    try:
        ## Uses the ALPHAVANTAGE API
        original = urllib.request.urlopen('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords='+msg+'&apikey=3VWEA280OOGR9AL4')
    except ValueError:
        print("\nInvalid Entry")
        start()
    data = json.load(original)

    best_match = [data['bestMatches'][0]['1. symbol'],data['bestMatches'][0]['9. matchScore']]
    return best_match

def get_data(sym,request_type):
    ## Returns the stock data requested by other functions
    
    try:
        ## Uses the IEX API
        original = urllib.request.urlopen('https://api.iextrading.com/1.0/stock/'+sym+'/'+request_type)
    except ValueError:
        print("\nInvalid Entry")
        start()
    data = json.load(original)
    if request_type == 'chart/dynamic':
        data = data['data']
    return data

def num(num):
    ## Edit large numbers (e.g. 1234567 to $1,234,567)
    try:
        num = '$'+str(format(num, ',d'))
    except:
        num = 'Unavailable'
    return num

def stock_info(stock):
    ## Returns general info about stock (the most basic feature)
    
    data = get_data(stock,'book')
    data_company = get_data(stock,'company')
    website = data_company['website']
    logo = get_data(stock,'logo')

    ## Shows the stock's latest price, the time of quote, and website url
    info = [data['quote']['close'],data['quote']['latestTime'],logo['url']]
    return info

def stock_describe(stock):
    ## Returns info for stock description
    
    data = get_data(stock,'company')
    website = data['website']+'/'
    try:
        website = website.replace('http://','https://')
    except:
        pass
    
    data2 = get_data(stock,'stats')
    exdividend = data2['exDividendDate']
    if data2['exDividendDate'] == 0:
        exdividend = 'None'
    
    ## Shows the stock's name, CEO, sector, industry and description
    info = [data['companyName'],website,'CEO',data['CEO'],'Sector',data['sector'],'Industry',data['industry']]
    info2 = ['Ex-dividend Date',exdividend,'Beta',str(round(data2['beta'],2)),'52 Week High-Low',str(data2['week52high'])+'-'+str(data2['week52low']),'MA50-MA200',str(round(data2['day50MovingAvg'],2))+'-'+str(round(data2['day200MovingAvg'],2))]
    return info,info2

def stock_income(stock):
    ## Return info for stock income statement
    
    data = get_data(stock,'financials?period=annual')
    data2 = get_data(stock,'company')

    info = [data2['companyName'],'https://seekingalpha.com/symbol/'+stock+'/income-statement','Operating Revenue',num(data['financials'][0]['operatingRevenue']),'Gross Profit',num(data['financials'][0]['grossProfit']),'Operating Income',num(data['financials'][0]['operatingIncome'])]
    info2 = ['Operating Expense',num(data['financials'][0]['operatingExpense']),'Net Income',num(data['financials'][0]['netIncome']),"R&D",num(data['financials'][0]['researchAndDevelopment']),'Report Date',data['financials'][0]['reportDate']] 
    
    return info,info2

def stock_balance(stock):
    ## Return the info for stock balance sheet

    global data

    data = get_data(stock,'financials?period=annual')
    data2 = get_data(stock,'company')
    website = data2['website']+'/'
    try:
        website = website.replace('http://','https://')
    except:
        pass

    info = [data2['companyName'],'https://seekingalpha.com/symbol/'+stock+'/balance-sheet','Cash Flow',num(data['financials'][0]['cashFlow']),'Shareholder Equity',num(data['financials'][0]['shareholderEquity']),'Total Assets',num(data['financials'][0]['totalAssets'])]
    info2 = ['Total Cash',num(data['financials'][0]['totalCash']),'Current Debt',num(data['financials'][0]['currentDebt']),'Total Debt',num(data['financials'][0]['totalDebt']),'Report Date',data['financials'][0]['reportDate']]    

    return info,info2    

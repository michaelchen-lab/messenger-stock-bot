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

def percent(num):
    try:
        return str(num)+'%'
    except:
        return 'Unavailable'

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

    def ceo(ceo):
        if ceo == '':
            return '-'
        else:
            return ceo
    
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
    info = [data['companyName'],website,'CEO',ceo(data['CEO']),'Sector',data['sector'],'Industry',data['industry']]
    info2 = ['Ex-dividend Date',exdividend,'Beta',str(round(data2['beta'],2)),'52 Week High-Low',str(data2['week52high'])+'-'+str(data2['week52low']),'MA50-MA200',str(round(data2['day50MovingAvg'],2))+'-'+str(round(data2['day200MovingAvg'],2))]
    return info,info2

def find_dividend(data):
    
    dates,dividends = [],[]
    data = data['Time Series (Daily)']
    for date in data:
        if data[date]['7. dividend amount'] != '0.0000':
            dates.append(date)
            dividends.append(data[date]['7. dividend amount'])

    return dates,dividends

def payout_frequency(dates):

    ## Find the frequency of dividend payment
    previous_year = int(dates[0][:-6])-1
    frequency = 0
    for x in dates:
        if int(x[:-6]) == previous_year:
            frequency += 1

    return frequency

def stock_dividend(stock):
    ## Returns info for stock dividend

    global data3

    try:
        ## Uses the ALPHAVANTAGE API
        original = urllib.request.urlopen('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&symbol='+stock+'&apikey=3VWEA280OOGR9AL4')

    except ValueError:
        print("\nInvalid Entry")
        start()
    data = json.load(original)
    data2 = get_data(stock,'stats')
    data3 = get_data(stock,'earnings')

    price = get_data(stock,'price')
    dates,dividends = find_dividend(data)
    frequency = payout_frequency(dates)

    exdividend_date = data2['exDividendDate'][:-11]
    if frequency == 12:
        dividend_frequency = 'Monthly'
    elif frequency == 4:
        dividend_frequency = 'Quarterly'
    elif frequency == 2:
        dividend_frequency = 'Biannually'
    elif frequency == 1:
        dividend_frequency = 'Annually'
    else:
        dividend_frequency = 'Unavailable'
    annual_payout = round(float(dividends[0])*frequency,2)
    dividend_yield = str(round((annual_payout/float(price))*100,2))+'%'
    annual_eps = float(data3['earnings'][0]['actualEPS'])+float(data3['earnings'][1]['actualEPS'])+float(data3['earnings'][2]['actualEPS'])+float(data3['earnings'][3]['actualEPS'])
    payout_ratio = str(round((annual_payout/annual_eps)*100,2))+'%'

    info = [data2['companyName'],'https://seekingalpha.com/symbol/'+stock+'/dividends/scorecard','Ex-dividend Date',exdividend_date+' ('+dividend_frequency+')','Dividend Yield: '+dividend_yield,'Annual Payout: '+str(annual_payout),'Payout Ratio',payout_ratio]
    return info

def stock_valuation(stock):
    ## Return info for stock valuation

    data = get_data(stock,'financials?period=annual')
    data2 = get_data(stock,'stats')
    data3 = get_data(stock,'earnings')
    data4 = get_data(stock,'company')

    price = get_data(stock,'price')
    try:
        eps = data3['earnings'][0]['actualEPS']+data3['earnings'][1]['actualEPS']+data3['earnings'][2]['actualEPS']+data3['earnings'][3]['actualEPS']
    except:
        eps = 'Unavailable'
    try:
        pe_ratio = round(price/eps,2)
        if pe_ratio < 0: ## P/E cannot be 0
            pe_ratio = '-'
    except:
        pe_ratio = 'Unavailable'
    try:
        debt_equity = round(data['financials'][0]['totalDebt']/data['financials'][0]['shareholderEquity'],2)
    except:
        debt_equity = 'Unavailable'
    try:
        price_cashflow = round(data2['marketcap']/data['financials'][0]['cashFlow'],2)
        if price_cashflow < 0: ## P/Cash Flow cannot be 0
            price_cashflow = '-'
    except:
        price_cashflow = 'Unavailable'
            
    info = [data4['companyName'],'https://seekingalpha.com/symbol/'+stock+'/valuation','Market Cap.',num(data2['marketcap']),'Price/Earnings Ratio (P/E)',str(pe_ratio),'Return on Equity (ROE)',percent(data2['returnOnEquity']),]
    info2 = ['Price/Sales Ratio (P/S)',str(round(data2['priceToSales'],2)),'Price/Book Ratio (P/B)',str(data2['priceToBook']),'Price/Cash Flow Ratio',str(price_cashflow),'Debt-to-Equity',str(debt_equity)]

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

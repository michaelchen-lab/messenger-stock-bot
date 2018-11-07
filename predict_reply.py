import pandas as pd
import os
import sys
import stock_data as sd

greeting=(["What's up!","Hey, nice to meet you!","Hi, it's good to hear from you again!"])
def classify(msg):
    
    if " " not in msg:
        ## when the user enters a company name or ticker symbol
        match = best_match(msg)
        info = stock_info(match[0])
        return ["$"+str(info[0])+" (as of "+info[1]+")",info[2]],match[0],'',"symbol",2
    
    elif "description" in msg or "Description" in msg:
        ## when the user asks for the description of a company
        try:
            msg = msg.replace('description','')
        except:
            msg = msg.replace('Description','')

        match = best_match(msg.strip())
        info = stock_describe(match[0])
        return info,match[0],'','list',2

    elif "dividends" in msg or "dividend" in msg or "Dividend" in msg:
        ## when the asks for the dividend of a company
        if "dividends" in msg:
            msg = msg.replace('dividends','')
        elif "dividend" in msg:
            msg = msg.replace('dividend','')
        elif "Dividend" in msg:
            msg = msg.replace('Dividend','')

        match = best_match(msg.strip())
        info = stock_dividend(match[0])
        return info,match[0],'','dividend',1

    elif "valuation" in msg or "Valuation" in msg or "value" in msg or "Value" in msg:
        ## when the user asks for the valuation of a company
        if "valuation" in msg or "Valuation" in msg:    
            try:
                msg = msg.replace('valuation','')
            except:
                msg = msg.replace('Valuation','')
        else:
            try:
                msg = msg.replace('value','')
            except:
                msg = msg.replace('Value','')

        match = best_match(msg.strip())
        info,info2 = stock_valuation(match[0])
        return info,info2,'','list',2

    elif "income" in msg or "Income" in msg:
        ## when the user asks for the income statement of a company
        try:
            msg = msg.replace('income','')
        except:
            msg = msg.replace('Income','')
        ## in case user adds 'statement'
        try:
            msg = msg.replace('statement','')
        except:
            pass
        try:
            msg = msg.replace('Statement','')
        except:
            pass
        
        match = best_match(msg.strip())
        info,info2 = stock_income(match[0])
        return info,info2,'','list',2

    elif "balance" in msg or "Balance" in msg:
        ## when the user asks for the balance sheet of a company
        try:
            msg = msg.replace('balance','')
        except:
            msg = msg.replace('balance','')
        ## in case user adds 'sheet'
        try:
            msg = msg.replace('sheet','')
        except:
            pass
        try:
            msg = msg.replace('Sheet','')
        except:
            pass
        
        match = best_match(msg.strip())
        info,info2 = stock_balance(match[0])
        return info,info2,'','list',2

    return "Sorry, I don't understand you.","","","other",1

## Link to stock_data.py
def best_match(msg):
    return sd.stock_match(msg)
def stock_info(stock):
    return sd.stock_info(stock)
def stock_describe(stock):
    return sd.stock_describe(stock)
def stock_income(stock):
    return sd.stock_income(stock)
def stock_balance(stock):
    return sd.stock_balance(stock)
def stock_valuation(stock):
    return sd.stock_valuation(stock)
def stock_dividend(stock):
    return sd.stock_dividend(stock)

## for testing purposes
if __name__ == '__main__':
    while(1):
      msg=input("Enter something: ")
      print(classify(msg))	

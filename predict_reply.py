import pandas as pd
import os
import sys
import stock_data as sd

greeting=(["What's up!","Hey, nice to meet you!","Hi, it's good to hear from you again!"])
def classify(msg):
    
    if " " not in msg:
        ## when the user enters a company name or ticker symbol
        match = best_match(msg)
        if match == []:
            return "Sorry, I don't understand you.","","","other",1
        info = stock_info(match[0])
        return "$"+str(info[0])+" (as of "+info[1]+")",match[0],info[2],"symbol",1
    
    elif "description" in msg or "Description" in msg:
        ## when the user asks for the description of a company
        try:
            msg = msg.replace('description','')
        except:
            msg = msg.replace('Description','')
        match = best_match(msg.strip())
        return stock_describe(match[0]),'','','list',1

    elif "income" in msg or "Income" in msg:
        ## when the user asks for the income statement of a company
        try:
            msg = msg.replace('income','')
        except:
            msg = msg.replace('Income','')
        match = best_match(msg.strip())
        info,info2 = stock_income(match[0])
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

if __name__ == '__main__':
    while(1):
      msg=input("Enter something: ")
      print(classify(msg))	

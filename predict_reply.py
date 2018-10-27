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
            return "Sorry, I don't understand you.","",""
        info = stock_info(match[0])
        print(info)
        return "$"+str(info[0])+" (as of "+info[1]+")",match[0],info[2],'symbol'
    
    elif "description" in msg or "Description" in msg:
        ## when the user asks for the description of a company
        try:
            msg = msg.replace('description','')
        except:
            msg = msg.replace('Description','')
        msg = msg.strip()
        match = best_match(msg)
        return stock_describe(match[0]),'','','list'

    return "Sorry, I don't understand you.","",""

## Link to stock_data.py
def best_match(msg):
    return sd.stock_match(msg)
def stock_info(stock):
    return sd.stock_info(stock)
def stock_describe(stock):
    return sd.stock_describe(stock)

if __name__ == '__main__':
    while(1):
      msg=input("Enter something: ")
      print(classify(msg))	

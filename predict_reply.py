import pandas as pd
import os
import sys
import stock_data as sd

greeting=(["What's up!","Hey, nice to meet you!","Hi, it's good to hear from you again!"])
def classify(msg):
    
    ##When msg is just one word, we assume the user sent a company name or symbol
    if " " not in msg:
        match = best_match(msg)
        if match == []:
            return "Sorry, I don't understand you."
        info = sd.stock_info(match[0])
        print(info)
        return "$"+str(info[0])+" (as of "+info[1]+")",match[0],info[2]       

    return "Sorry, I don't understand you.","",""

def best_match(msg):
    return sd.stock_match(msg)

if __name__ == '__main__':
    while(1):
      msg=input("Enter something: ")
      print(classify(msg))	

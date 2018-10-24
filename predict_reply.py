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
        if 'AM' in info[1] or 'PM' in info[1]:
            return "The price of "+match[0]+" at "+info[1]+" is $"+str(info[0])+"."
        else:
            return "The price of "+match[0]+" in "+info[1]+" is $"+str(info[0])+"."
        

    return "Sorry, I don't understand you."

def best_match(msg):
    return sd.stock_match(msg)

if __name__ == '__main__':
    while(1):
      msg=input("Enter something: ")
      print(classify(msg))	


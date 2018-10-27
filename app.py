import os
import sys
import json
import predict_reply

import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ.get("VERIFY_TOKEN",None):
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events
  try:
    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    received_message(recipient_id)
                    try: 
                        message_text = messaging_event["message"]["text"]  # the message's text
            
                        reply,extra1,extra2,mode = predict(message_text)
                        print('done')
                        send_message(sender_id, reply,str(extra1),str(extra2),mode)
                    except:
                        send_message(sender_id,str("Sorry! I didn't get that."),"","","other")    
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200
  except:
    pass  

def received_message(recipient_id):
    log("Message received from {recipient}".format(recipient=recipient_id))

def send_message(recipient_id, message_text,extra1,extra2,mode):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ.get("PAGE_ACCESS_TOKEN",None)
    }
    headers = {
        "Content-Type": "application/json"
    }
    if mode == 'other':
        ## When the bot is not sending stock messages
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            }
        })
    elif mode == 'symbol':
        ## When sending information on a stock
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "attachment":{
                    "type":"template",
                    "payload":{
                        "template_type":"generic",
                        "elements":[
                            {
                            "title": extra1,
                            "subtitle": str(message_text),
                            "buttons": [
                                {
                                    "type":"postback",
                                    "title":"Description",
                                    "payload": extra1+" description"
                                },{
                                    "type":"postback",
                                    "title":"Financials",
                                    "payload": extra1+" financials"
                                }
                            ]
                            }
                        ]
                    }
                }
            }
        })
    elif mode == 'list':
        ## When sending description of stock 
        data = json.dumps({
            "recipient":{
                "id": recipient_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "list",
                        "top_element_style": "compact",
                        "elements": [
                            {
                                "title": reply[0],
                                "buttons": [
                                    {
                                        "title": "View website",
                                        "type": "web_url",
                                        "url": reply[1]
                                    }
                                ]       
                            },
                            {
                                "title": reply[2],
                                "subtitle": reply[3]
                            },
                            {
                                "title": reply[4],
                                "subtitle": reply[5]
                            },
                            {
                                "title": reply[6],
                                "subtitle": reply[7]
                            },
                            {
                                "title": reply[8],
                                "subtitle": reply[9]
                            }
                        ]
                    }
                }
            }
        })
        
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print(str(message))
    sys.stdout.flush()

## Link to predict_reply.py
def predict(incoming_msg):
    reply,extra1,extra2 = predict_reply.classify(incoming_msg)
    return reply,extra1,extra2

if __name__ == '__main__':
    app.run(debug=True)
    #print(predict(raw_input("Enter something")))

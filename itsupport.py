import os
import time
import json
import re
import sys
import requests
import trend
import client
from slackclient import SlackClient
from ln2sql import interface
# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# instantiate Slack
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_channel = 'D77U8FKV3'

sys.path.append(os.path.join(os.getcwd(),'..','..'))
import watson_developer_cloud
USERNAME = os.environ.get('CONVERSATION_USERNAME','20e6e394-e5cc-4191-b05d-657594ac2535')
PASSWORD = os.environ.get('CONVERSATION_PASSWORD','t8QzQAXgSHFX')
conversation = watson_developer_cloud.ConversationV1(username=USERNAME,
                                                     password=PASSWORD,
                                                     version='2017-04-21')


workspaceid2 = '62891bb2-84b0-4d98-8dc2-bb1ea0c6bad2'
workspaceid1 = '78f78e3b-1cb3-4b95-a846-a4c4ce3c7c17'
workspace2 = conversation.get_workspace(workspace_id=workspaceid2)

import MySQLdb
db = MySQLdb.connect("localhost","root","the c-13","megathon")

def parse_slack_output(output_list) :
    if output_list and len(output_list) > 0:
        if "bot_id" in output_list[0] :
            # print("FOUND BOT ID")
            return None,None
        for output in output_list:
            if output and 'text' in output :
                # return text after the @ mention, whitespace removed
                return output['text'].strip().lower(), output['channel']
    return None, None

def getmsgfromuser() :
    READ_WEBSOCKET_DELAY = 0.02
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel :
                return command
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

def sendmsgtouser(msg) :
    if slack_client.rtm_connect():
        print("StarterBot connected and running! --- ready to send msg")
        slack_client.api_call("chat.postMessage",channel=slack_channel,text=msg)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

def learnintent(msg,workspaceid) :
    print("was unable to indentify the intent")
    sendmsgtouser("Bot was unable to understand what u asked him. Please help him train.\nTry out some other words that might help.")
    msg = getmsgfromuser()
    # print("msg = ",msg)
    message_input = {'text': msg}
    response = conversation.message(workspace_id=workspaceid,message_input=message_input)
    if(len(response['intents']) == 0) :
        valid = learnintent(msg,workspaceid)
    else : valid = response['intents'][0]['intent']
    # print("m = ",msg," v = ",valid)
    # conversation.create_example(workspace_id=workspaceid,intent=valid,text=msg)
    return valid

def learnentity(msg) :
    print("was unable to indentify the entities")
    pass

def processquery2(msg) :
    message_input = {'text': msg}
    response = conversation.message(workspace_id=workspaceid2,message_input=message_input)

    if(len(response['intents']) == 0) :
        myintent = learnintent(msg,workspaceid2)
    else :
        myintent = response['intents'][0]['intent']

    if(len(response['entities']) == 0) :
        learnentity(msg)
    # print(msg)
    # print(response['entities'])
    # print(response['intents'])
    intent = response['intents'][0]['intent']
    entities = [ {"e":response['entities'][i]['entity'],"v":response['entities'][i]["value"]} for i in range(len(response['entities']))]
    return intent , entities

def processquery1(msg) :
    message_input = {'text': msg}
    response = conversation.message(workspace_id=workspaceid1,message_input=message_input)

    if(len(response['intents']) == 0) :
        myintent = learnintent(msg,workspaceid1)
    else :
        myintent = response['intents'][0]['intent']

    sendmsgtouser("Classified query as : " + myintent)
    return myintent

def makequery(msg) :
    # Create a Cursor object to execute queries.
    cur = db.cursor()

    # Select data from table using SQL query.
    cur.execute(msg)
    reply = ""
    # print(cur.fetchall())
    for row in cur.fetchall() :
        for i in range(len(row)) :
            reply += str(row[i]) + " "
        reply += "\n"
    return reply

def handlebasic(msg) :
    temp = interface.sql_string(msg)
    temp = re.sub(r'\x1b\[[0-9]m', '  ',temp )
    temp = ' '.join(temp.split('\n'))
    print("t = ",temp)
    # intent, E = processquery2(msg)
    # f1 = E[0]["e"]
    # f2 = E[1]["e"]
    # f2v = E[1]["v"]
    # print(E)
    return makequery(temp)

def handlesentiment(msg) :
    msg = msg.split(' ')
    if "distribution" in msg :
        l = 0
        while(l < len(msg) and msg[l] != 'client') : l += 1
        r = l
        while(r < len(msg) and msg[r] != 'based') : r += 1
        ans = ' '.join(msg[l+1:r])
        print("client name is "+ans)
        client.client_analysis(ans)
        my_file = {'file' : ('./graph2.png', open('./graph2.png', 'rb'), 'png')}
        slack_client.api_call('files.upload', channels=[slack_channel], filename='graph2.png', file= open('./graph2.png', 'rb'))
        payload={ "filename":"graph2.png","token":os.environ.get('SLACK_BOT_TOKEN'),"channels":[slack_channel],}
        r = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)
        return ""
    else : return "Invalid Query"



def handletrend(msg) :
    msg = msg.split(' ')
    if "ticket" in msg :
        l = 0
        while(msg[l] != "ticket") : l += 1
        ans = msg[l+1]
        trend.trend_analysis(int(ans))
        my_file = {'file' : ('./graph.png', open('./graph.png', 'rb'), 'png')}
        slack_client.api_call('files.upload', channels=[slack_channel], filename='graph.png', file= open('./graph.png', 'rb'))
        payload={ "filename":"graph.png","token":os.environ.get('SLACK_BOT_TOKEN'),"channels":[slack_channel],}
        r = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)
        return ""

    elif "client" in msg :
        l = 0
        while(l < len(msg) and msg[l] != 'client') : l += 1
        r = l
        while(r < len(msg) and msg[r] != 'based') : r += 1
        ans = ' '.join(msg[l+1:r])

    else : return "Invalid Query"
if __name__ == "__main__":
    # Q = [ "how many tickets are open ?",
    #          "how many tickets have low proiority ?",
    #         #  "What is the median ticket number for google test ?",
    #          "what is the average time spent on tickets ?",
    #         #  "What percentage of tickets are still open ?",
    #          "What is the max time spent on closed tickets ?",
    #         #  "Give me the volume of tickets with positive tone on monthly basis for YTD?",
    #          "What is the number of tickets raised by ltd ?",
    #          "how many tickets were raised by ltd ?",
    #          "how many tickets by google are still open ?",
    #     ]

    # my_file = {'file' : ('./1.png', open('./1.png', 'rb'), 'png')}
    # slack_client.api_call('files.upload', channels=[slack_channel], filename='1.png', file= open('./1.png', 'rb'))
    # payload={ "filename":"1.png","token":os.environ.get('SLACK_BOT_TOKEN'),"channels":[slack_channel],}
    # r = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

    # print(handlebasic("how many ticket of chatbot have status is equal to open"))
    print("The game has begin")
    while True :
        msg = getmsgfromuser()
        reply = "None"
        intent = processquery1(msg)
        if intent == 'basic' :
            reply = handlebasic(msg)
        elif intent == 'sentiment' :
            reply = handlesentiment(msg)
        elif intent == 'trend' :
            reply = handletrend(msg)
        if(reply and len(reply) > 0) : sendmsgtouser("ans to the query is : " + reply)

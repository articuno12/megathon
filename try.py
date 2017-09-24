import json
import sys
import os
sys.path.append(os.path.join(os.getcwd(),'..','..'))
import watson_developer_cloud
USERNAME = os.environ.get('CONVERSATION_USERNAME','20e6e394-e5cc-4191-b05d-657594ac2535')
PASSWORD = os.environ.get('CONVERSATION_PASSWORD','t8QzQAXgSHFX')
conversation = watson_developer_cloud.ConversationV1(username=USERNAME,
                                                     password=PASSWORD,
                                                     version='2017-04-21')

def processquery2(in) :
    workspace_id = '62891bb2-84b0-4d98-8dc2-bb1ea0c6bad2'
    workspace = conversation.get_workspace(workspace_id=workspace_id)
    message_input = {'text': in}
    response = conversation.message(workspace_id=workspace_id,message_input=message_input)

workspace_id = '78f78e3b-1cb3-4b95-a846-a4c4ce3c7c17'
# check workspace status (wait for training to complete)
workspace = conversation.get_workspace(workspace_id=workspace_id)
# print('The workspace status is: {0}'.format(workspace['status']))
# if workspace['status'] == 'Available':
#     print('Ready to chat!')
# else:
#     print('The workspace should be available shortly. Please try again in 30s.')
#     print('(You can send messages, but not all functionality will be supported yet.)')


Q = [ "how many tickets are open ?",
         "how many tickets have low proiority ?",
        #  "What is the median ticket number for google test ?",
         "what is the average time spent on tickets ?",
        #  "What percentage of tickets are still open ?",
         "What is the max time spent on closed tickets ?",
        #  "Give me the volume of tickets with positive tone on monthly basis for YTD?",
         "What is the number of tickets raised by ltd ?",
         "how many tickets were raised by ltd ?",
         "how many tickets by google are still open ?",
         ""
    ]

# start a chat with the pizza bot
for q in Q :
    message_input = {'text': q}
    response = conversation.message(workspace_id=workspace_id,
                                message_input=message_input)
    print("q = ",q)
    print(response["intents"])
    print(response["entities"])
# print(dir(response))
# print("88888888888888888888888888888888888888888888")
# print(json.dumps(response, indent=2))

# continue a chat with the pizza bot
# (when you send multiple requests for the same conversation,
#  then include the context object from the previous response)
# message_input = {'text': 'medium'}
# response = conversation.message(workspace_id=workspace_id,
#                                 message_input=message_input,
#                                 context=response['context'])
# print(json.dumps(response, indent=2))
print("sUCCESS")

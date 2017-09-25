import ast
import MySQLdb
import json
import os
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3
import matplotlib.pyplot as plt
db = MySQLdb.connect("localhost","root","the c-13","megathon")
cursor = db.cursor()


def trend_analysis(ticket_no):
    # print("ticket_no = ",ticket_no)
    tone_analyzer = ToneAnalyzerV3(
        username="cf8e860d-db2b-42d4-9cab-513221dc2665",
        password='uuVYsn4GPwRb',
        version='2016-05-19')
    query = "Select comments from chatbot where ticket= " + str(ticket_no)
    # ticket_no = int(ticket_no)
    cursor.execute(query)
    comments = cursor.fetchall()
    # print(comments)
    ans = []
    for c in comments[0][0].split(';'):
        a = c.split(':')[0]
        b = c.split(':')[1]
        ans.append({"text":b, "user":a })
    messages = {"utterances":ans}

    output = json.dumps(tone_analyzer.tone_chat(messages["utterances"]), indent=2)
    result = ast.literal_eval(output)
    print result
    num_of_tickets = len(result["utterances_tone"])
    negative = ["frustrated","sad","impolite"]
    positive = ["excited","satisfied"]
    neutral = ["neutral","polite"]
    res = []
    for i in range(0,num_of_tickets):
        t = result["utterances_tone"][i]["tones"]
        if len(t) == 0:
            res.append(0)
        else:
            tone = t[0]["tone_id"]
            if tone in negative:
                res.append(-1)
            if tone in positive:
                res.append(1)
            if tone in neutral:
                res.append(0)
    values = []
    for i in range(0,len(res)):
        values.append(i)
    # with open('data.json', 'w') as outfile:
    #     json.dump(messages, outfile)

    #data contains the json output
    # data
    print res
    axis = plt.gca()
    axis.set_ylim([-2,2])
    plt.plot(res)
    #plt.show()
    # import os
    # os.system("rm graph.png")
    plt.savefig('graph.png')
    plt.close()

# trend_analysis(872823810)

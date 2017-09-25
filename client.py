import ast
import MySQLdb
import json
import os
from os.path import join, dirname
from watson_developer_cloud import ToneAnalyzerV3
import matplotlib.pyplot as plt
db = MySQLdb.connect("localhost","root","the c-13","megathon")
cursor = db.cursor()

def client_analysis(client_name):
    n_num = 0 #negative
    p_num = 0 #positive
    l_num = 0 #neutral
    tone_analyzer = ToneAnalyzerV3(
        username="cf8e860d-db2b-42d4-9cab-513221dc2665",
        password='uuVYsn4GPwRb',
        version='2016-05-19')
    query = "Select comments from chatbot where client = \"" + str(client_name) + "\" "
    # ticket_no = int(ticket_no)
    cursor.execute(query)
    co = cursor.fetchall()
    #print co
    comments = co
    ans = []
    for c in comments:
        ans.append({"text": c[0] })
        if len(ans) > 49:
            break
        # print c[0]
    messages = {"utterances":ans}

    output = json.dumps(tone_analyzer.tone_chat(messages["utterances"]), indent=2)
    result = ast.literal_eval(output)
    # print result
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
                n_num += 1
            if tone in positive:
                res.append(1)
                p_num += 1
            if tone in neutral:
                res.append(0)
                l_num += 1

    p_num = 1
    total = n_num + l_num + p_num
    n = n_num*1.0/total * 360.0
    l = l_num * 1.0/total * 360.0
    p = p_num *1.0/total * 360.0
    labels = ["Negative","Positive","Neutral"]
    sizes = [n,p,l]
    explode = (0, 0, 0)
    colors = ['gold', 'yellowgreen', 'lightcoral']
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    import os
    os.system("rm graph2.png")
    plt.savefig('graph2.png')
    plt.close()
    # with open('data.json', 'w') as outfile:
    #     json.dump(messages, outfile)

    #data contains the json output
    # data
    # plt.scatter(X[:,0],X[:,1],c=y)

# client_analysis("YouTube")

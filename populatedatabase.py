import csv
f = open("./dataset_2.csv")
reader = csv.reader(f)
import MySQLdb
db = MySQLdb.connect("localhost","root","the c-13","megathon")
cursor = db.cursor()
i=0
for row in reader:
    if i==0:
        i+=1
    else:
        #print row
        cursor.execute("""INSERT INTO chatbot (ticket, status, severity, client, date_open,time,comments) VALUES(%s ,%s, %s,%s,%s,%s,%s)""", (int(row[0]),row[1],row[2],row[3],row[4],int(row[5]),row[6]))
        db.commit()
db.close()

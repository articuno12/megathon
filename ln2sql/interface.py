import os
import subprocess
def sql_string(sequence):
    bash_command = "python ln2sql.py -d database/chatbot.sql -l lang/english.csv -i " + '"' + sequence + '"' + " -t thesaurus/th_english.dat -j output.json"
    output = subprocess.check_output(['bash','-c', bash_command])
    return output
# print sql_string("how many Ticket the chatbot have Status is equal to open AND client is lesser than 12.12.2017")

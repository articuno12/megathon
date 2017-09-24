import os
import subprocess
def sql_string(sequence):
    # print(os.getcwd())
    bash_command = "python ln2sql/ln2sql.py -d ln2sql/database/chatbot.sql -l ln2sql/lang/english.csv -i " + '"' + sequence + '"' + " -t ln2sql/thesaurus/th_english.dat -j output.json"
    # os.system(bash_command + ">temp.txt")
    output = subprocess.check_output(['bash','-c', bash_command])
    return output
# print sql_string("how many Ticket the chatbot have Status is equal to open AND client is lesser than 12.12.2017")

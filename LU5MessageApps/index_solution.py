from flask import Flask, request, jsonify, render_template
import datetime
import os
import dialogflow
import requests
import json
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)   # get the incoming JSON structure
    action = data['queryResult']['action'] # get the action name associated with the matched intent
    
    if (action == 'test_connection'):
        return test_connection(data)
    
    #### TODO #1 : Match to the right action from dialogflow
    if (action == 'getQueueNr'):
        return get_queue(data)
    
    
def test_connection(data):
    reply = {}
    reply["fulfillmentText"] = "Greeting from webhook"
    return jsonify(reply)
    
      
def get_queue(data):
    
    #### TODO #2 : Extracts the parameters phone, name and aliments
    ###            Appends the original query string using the key 'queryText'
    
    phone  = data['queryResult']['parameters']['phone']
    name  = data['queryResult']['parameters']['name']
    reason = data['queryResult']['parameters']['aliments'] 
    reason += data['queryResult']["queryText"]
    
    today = datetime.date.today()          ### returns the current data    
    patient = (today, name, phone, reason) ### This tuple will be inserted into table 
    
    database = "./SQLiteDB/pythonsqlite.db" #### Connect to the database
    conn = create_connection(database)
    
    ### TODO #3: Use the connection call the function create_visits() to 
    ###          insert data (tuple patient) in the data.
    ###          The function will return a queue number based on auto increment
    
    with conn:
        queue_nr = create_visits(conn, patient)
        print ('The last queue number is ' + str(queue_nr))  ## for debugging only
    
    
    ### TODO #4: Prepares a response string
    response = "Dear {} , your queue number is {}. "  \
                "We will call you at {} 15 mins before " \
                "your turn is due. ".format(name, queue_nr, phone)
            
            
    reply = {}
    reply["fulfillmentText"] = ""
    reply["fulfillmentMessages"] = []
    
    
    ### TODO #5: Creates the message object for Telegram 
    ### .        

    msg_object = {}
    msg_object["platform"] = "TELEGRAM"

    ### TODO #6: Creates the custom payload with inline_keyboard
   
    msg_object["payload"] = {}
    msg_object["payload"]["telegram"] = {}
    msg_object["payload"]["telegram"]["text"] = response
    msg_object["payload"]["telegram"]["reply_markup"] =  {}
    msg_object["payload"]["telegram"]["reply_markup"]["inline_keyboard"] =  []
    
     ### TODO #7: Creates a keyboard row with two keys and append to the message object
        
    tg_keyboard_row = []
    tg_keyboard_row.append({"text" : "👍👍'", "callback_data": "acknowledges the queue number"})
    tg_keyboard_row.append({"text" : "😊😊", "callback_data": "acknowledges the queue number"})
    
    msg_object["payload"]["telegram"]["reply_markup"]["inline_keyboard"].append(tg_keyboard_row)

    reply["fulfillmentMessages"].append(msg_object)    
    
    return jsonify(reply)



### The two functions below are provided for you.
### It establish a connection to the database
### and inserts a row in the table VISITS

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None


def create_visits(conn, patient):
    """
    Create a new visit into the table VISITS
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO visits(visit_date, patient_name, patient_phone, visit_reason)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, patient)
    return cur.lastrowid



if __name__ == "__main__":
    app.run()
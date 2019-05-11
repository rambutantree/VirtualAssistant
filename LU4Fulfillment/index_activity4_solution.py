from flask import Flask, request, jsonify, render_template
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
    
    if (action == 'get_projectname'):
        return get_projectname(data)
    
    ######################################################
    ### TODO #1: identify the action as define in Dialogflow
    ### and call the function handler get_tasks_by_projectname
    
    if (action == 'get_task'):
        return get_tasks_by_projectname(data)

    
def get_projectname(data):
    response = "I am busy with:  "

    ### Establish a connection to the databse
    database = "./SQliteDB/pythonsqlite.db"
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects")
        rows = cur.fetchall()
        for row in rows:
            pname = row[1]    ### row is tuple. The project name is in the index [1]
            response += pname + " , "

    reply = {
        "fulfillmentText": " " ,
        "fulfillmentMessages" : [
            {
              "text" : {
                  "text" : [response]
              }    
            }
        ]
    }    
    return jsonify(reply)

#



def get_tasks_by_projectname(data):
  
    ######################################################
    ### TODO #2: Extract the project name from thefulfillment request
    
    projectname  = data['queryResult']['parameters']['projectname']

    database = "./SQliteDB/pythonsqlite.db"
    conn = create_connection(database)
 

    with conn:
    ######################################################
    ### TODO #3: Extract the project name in the fulfilment request JSON object 
    ### a) Create a cursor to the connection
    ### b) Create a sql string to select projectname and join tasks and projects tables, linked by projectname and project_id

        cur = conn.cursor()
        sql = "SELECT p.name, t.name, t.status_id, t.begin_date FROM tasks t, projects p "
        sql += "WHERE p.id = t.project_id AND p.name = '" + projectname + "'"
        cur.execute(sql)
        rows = cur.fetchall()

        #################################################
        ### TODO #4: Checks if there are rows returned.
        ### If no, insert the first message into reponse list.
        ### If yes, insert the first message and the tasks into the
        ### the response list
        
        
        response_list = []
        if len(rows) == 0:
           response = "No task found for project " + projectname
           response_list.append({'text': {'text': [response]}})
           
           
        else:
           response = "Tasks for project "  + projectname + " are :"
           response_list.append({'text': {'text': [response]}})
           for row in rows:
               response = {  "text": { "text": [row[1]]}  }
               response_list.append(response)
            
            

    #####################################################
    ### TODO #5: Prepare a dictionary to insert the 
    ### key-value pairs. The list from the previous step
    ### is used
    
    reply = {}
    reply["fulfillmentText"] = " "
    reply["fulfillmentMessages"] = response_list
      
    return jsonify(reply)



### function for DB connection
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None
 


if __name__ == "__main__":
    app.run()
from flask import Flask, request, jsonify, render_template
import os
import dialogflow
import requests
import json

### for task 5 solution

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

    
def get_projectname(data):
    response = "I am busy with ... "
######################################################
### TODO #2: Establish a conneect to the databse
###          and fetch project information

    database = "./SQliteDB/pythonsqlite.db"
    conn = create_connection(database)
    
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects")
        rows = cur.fetchall()
        for row in rows:
            pname = row[1]                        ### row is tuple. The project name is in the index [1]
            response += pname + " , "
        
##########################################################
### TODO #3 : Move the string response into the dictionary
###
    reply = {
        "fulfillmentText": " " ,
        "fulfillmentMessages" : [
            {
              "text" : {
                  "text" : [ response ]
              }    
            }
        ]
    }    
    return jsonify(reply)



######################################################
### TODO #1: Create a function for DB connection
""" create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
"""
######################################################

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None
 

if __name__ == "__main__":
    app.run()
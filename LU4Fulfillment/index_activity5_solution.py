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
      
    if (action == 'try_fulfillment_msgs'):
        return fulfillment_msgs(data)
    
    
      
def fulfillment_msgs(data):
    
    ##################################################################
    ### TODO #1: Initialize the dictionaries
    ###          for the two keys fulfillmentMessages
    ###          and fulfillmentText
    ##################################################################
    reply = {}
    reply["fulfillmentText"] = " "
    reply["fulfillmentMessages"] = []
    msgs = []
    
    #################################################
    ### TODO #2: To prepare a single line response
    ### append {'text': {'text': [  "My hobby is reading and dancing"]}} to msgs structure
    
    msgs.append({'text': {'text': [  "My hobby is reading and dancing"]}})
    
    
    
    ######################################################
    ### TODO #3: To prepare two fix lines response
    ### append {'text': {'text': [  "My hobby is reading "]}} to to msgs structure
    ### append {'text': {'text': [  "and dancing "]}} to to msgs structure     
    
    #msgs.append({'text': {'text': [  "My hobby is reading "]}})
    #msgs.append({'text': {'text': [  "and dancing "]}})
            
    
    ###############################################################
    ### TODO #4: Assign the list msgs to the fulfillmentMessage key
    
    reply["fulfillmentMessages"] = msgs  
    return jsonify(reply)



### function for DB connection


if __name__ == "__main__":
    app.run()
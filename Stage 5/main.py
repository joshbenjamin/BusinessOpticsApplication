from __future__ import print_function
import sqlite3
import os
import time
import sys
from flask import Flask, request, render_template, g, session, redirect, url_for
import requests

app = Flask(__name__) # Instantiates a flask project
app.secret_key = os.urandom(24) # Generates a secret key to be used with the session data

@app.route("/")   # Root
def index():
    return "Hello World"

@app.route("/api/update", methods=["POST"])  # Used to submit asynchronously
def JSCall():
    name = form.request['name']
    number = form.request['emptyField']  # Takes in the values from the form
    newInsert(name, number) # Inserts values into DB
    return account(name) # Reloads page we want to see

@app.route("/account/<name>", methods=["POST", "GET"]) #Page we view for balances
def account(name):
    
    if 'addElement' in session:
        newInsert(name, session['addElement'])  #If there is a value in session, we use it and pop it off
        session.pop('addElement', None)    
    
    cursor = get_db().execute("SELECT Date, Balance FROM accounts WHERE Name = '" + name + "'")
    
    results = cursor.fetchall()   # Getting values from the DB to render
    cursor.close()
    
    response = requests.get("https://api.mybitx.com/api/1/ticker?pair=XBTZAR") # Gets the current BTC price
    btcPrice = response.json()["last_trade"]    
    
    entries = [] 
    
    for entry in results: # Used so we can render results
        entries.append({"date":entry[0], "randAmount":entry[1], "btcAmount":("%.6f" % (entry[1]/float(btcPrice)))})
    
    numEntries = len(entries)
    
    if request.method == 'POST': #When a new entry is submitted, it goes here
        session['addElement'] = request.form['addElement']
        return redirect(url_for('account', name=name))      
    
    return render_template("account.html", entries=entries, name=name, numEntries=numEntries, btcPrice=btcPrice)
    
def newInsert(name, newNumber): # Inserts a value in the DB for the person's name
    with sqlite3.connect('accounts.db') as newConnection:
        curs = newConnection.cursor()
        
        curs.execute("INSERT INTO accounts VALUES ('" + name + "', '" + time.strftime("%Y-%m-%d") + "', " + newNumber + ")")
        
        newConnection.commit # Commits so that the DB is saved 
        curs.close()        


def get_db():
    db = getattr(g, '_database', None)
    
    if db is None: # Retrieves the database
        db = g._database = sqlite3.connect("accounts.db")
    return db

if __name__ == '__main__': # Runs this application as the main class
    app.run(debug=True, host='0.0.0.0', port=1234) # Specifies at port 1234 of 0.0.0.0 or localhost
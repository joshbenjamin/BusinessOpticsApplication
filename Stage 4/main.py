from __future__ import print_function
import sqlite3
import os
import time
import sys
from flask import Flask, request, render_template, g, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    return "Hello World"

@app.route("/account/<name>", methods=["POST", "GET"])
def account(name):
    
    if 'addElement' in session:
        newInsert(name, session['addElement'])
        session.pop('addElement', None)    
    
    
    
    cursor = get_db().execute("SELECT Date, Balance FROM accounts WHERE Name = '" + name + "'")
    
    results = cursor.fetchall()
    cursor.close()
    
    response = requests.get("https://api.mybitx.com/api/1/ticker?pair=XBTZAR")
    btcPrice = response.json()["last_trade"]    
    
    entries = []
    
    for entry in results:
        entries.append({"date":entry[0], "randAmount":entry[1], "btcAmount":("%.6f" % (entry[1]/float(btcPrice)))})
    
    numEntries = len(entries)
    
    
    
    if request.method == 'POST':
        session['addElement'] = request.form['addElement']
        return redirect(url_for('account', name=name))      
    
    return render_template("account.html", entries=entries, name=name, numEntries=numEntries, btcPrice=btcPrice)

    
def newInsert(name, newNumber):
    with sqlite3.connect('accounts.db') as newConnection:
        curs = newConnection.cursor()
        
        curs.execute("INSERT INTO accounts VALUES ('" + name + "', '" + time.strftime("%Y-%m-%d") + "', " + newNumber + ")")
        newConnection.commit
        curs.close()        


def get_db():
    db = getattr(g, '_database', None)
    
    if db is None:
        db = g._database = sqlite3.connect("accounts.db")
    return db

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)
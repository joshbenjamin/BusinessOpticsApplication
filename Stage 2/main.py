import sqlite3
from flask import Flask, request, render_template, g

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/account/<name>", methods=["POST", "GET"])
def account(name):
    
    entries = []
    
    cursor = get_db().execute("SELECT Date, Balance FROM accounts WHERE Name = '" + name + "'")
    
    results = cursor.fetchall()
    cursor.close()
    
    for entry in results:
        entries.append({"date":entry[0], "randAmount":entry[1]})
    
    numEntries = len(entries)
    
    return render_template("account.html", entries=entries, name=name, numEntries=numEntries)


def get_db():
    db = getattr(g, '_database', None)
    
    if db is None:
        db = g._database = sqlite3.connect("accounts.db")
    return db

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1234)
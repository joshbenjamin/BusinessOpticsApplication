import sqlite3

with sqlite3.connect("accounts.db") as connection:
    cursor = connection.cursor()
    
    cursor.execute(""" DROP TABLE accounts """)
    
    cursor.execute(""" 
    
    CREATE TABLE accounts(Name TEXT, Date TEXT, Balance NUMBER)
    
    """)
    
    cursor.execute('INSERT INTO accounts VALUES ("James", "2017-01-01", 40)')
    cursor.execute('INSERT INTO accounts VALUES ("James", "2017-02-01", 22)')
    cursor.execute('INSERT INTO accounts VALUES ("James", "2017-03-01", 56)')
    cursor.execute('INSERT INTO accounts VALUES ("Josh", "2017-01-01", 2)')
    cursor.execute('INSERT INTO accounts VALUES ("Satoshi", "2017-01-01", 9999999)')
#!/usr/bin/python
from flask import Flask, render_template, request
import datetime
import sys
import os
import mariadb

app = Flask(__name__)

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="frank",
        password="password",
        host="localhost",
        database="datalog"
        )

except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


# Query table
try:
    cur.execute("SELECT * FROM thlog")
    
    # Print Result-set
    for (time, temperature, humidity) in cur:
        print(time,temperature, humidity)
except mariadb.Error as e:
    print(f"Error: {e}")

print(f"Last Inserted ID: {cur.lastrowid}")

# Close Connection
conn.close()

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   return render_template('index.html', **templateData)


@app.route("/date", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if not request.form.get("date") or not request.form.get("calculate"):
            return render_template("failure.html")
        
        return render_template("greet.html", name=request.form.get("name", "world"))
    
    else:
        return render_template("index.html")

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
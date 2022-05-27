#!/usr/bin/python
from flask import Flask, render_template, request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology
import datetime
import sys
import os
import mariadb

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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




# Close Connection
# conn.close()

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
        else:
            
            # Query table
            try:
                cur.execute("SELECT time,temperature from thlog where temperature = (SELECT MAX(temperature) FROM thlog WHERE time BETWEEN ? AND ?)", date)
                # Print Result-set
                for (time, temperature) in cur:
                    print(time,temperature)
            
            except mariadb.Error as e:
                print(f"Error: {e}")

            return render_template("greet.html", name=request.form.get("name", "world"))
    
    else:
        return render_template("index.html")



def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

#!/usr/bin/python
from flask import Flask, render_template, request, jsonify, Response
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology
import datetime
import sys
import os
import mariadb
import cv2
from gpiozero import LED
import time
from subprocess import call

# import pytz

led = LED(3)
led.off()
light_status = False

app = Flask(__name__)

#initializing camera
camera = cv2.VideoCapture(-1)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/", methods=["GET", "POST"])
def index():
        
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
            cur.execute("SELECT * FROM thlog2 ORDER BY id DESC LIMIT 100")
            datalogs = []
            
            
            for (temperature, humidity, time, id) in cur:
                
                datalogs.append({"temperature":str(format(round(temperature, 2), '.2f')) + " °F",
                                    "humidity":str(format(round(humidity, 2), '.2f')) + " %",
                                    "time":time,
                                    "id":id
                        })
            
        
        #     # Creating dictionary to send back in JSON form
        #     info = {"temperature":str(round(temperature, 2)) + " °F",
        #         "humidity":str(round(humidity, 2)) + " %",
        #         "time":time,
        #         "id":id
        #     }
        #     print(info)
        
        except mariadb.Error as e:
                    print(f"Error: {e}")
        
        # Close Connection
        conn.close()

        
        return render_template("index.html", datalogs=datalogs)


@app.route("/analysis", methods=["POST", "GET"])
def analysis():
# Data Analysis
        print("INSIDE ANALYSssssIS")
        date = request.form
        print(date)
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

        if not request.form.get("date") or not request.form.get("calculate"):
            print("Inside Failure")
            return render_template("failure.html")
        else:
            
            # Query table
            try:
                date = request.form.get("date")
                date2 = request.form.get("date2")
                method = request.form.get("data").lower()
                calculate = request.form.get("calculate").lower()
                
                print(date, date2, method, calculate)
                
                if calculate == "maximum":
                    calculate = "MAX"
                elif calculate == "minimum":
                    calculate = "MIN"
                else:
                    calculate = "AVG"
    
                query = f"SELECT * from thlog2 where {method} = (SELECT {calculate}({method}) FROM thlog2 WHERE time BETWEEN '{date}' AND '{date2}')"
                
                print(query)

                cur.execute(query)
                
                for (temperature, humidity, time, id) in cur:
                    pass
                
                # Creating dictionary to send back in JSON form
                info = {"temperature":str(format(round(temperature, 2), '.2f')) + " °F",
                    "humidity":str(format(round(humidity, 2), '.2f')) + " %",
                    "time":time,
                    "id":id
                }
            
            except mariadb.Error as e:
                 print(f"Error: {e}")

            print(info)
            # Close Connection
            conn.close()

            return jsonify(info) # returning a JSON response
            
@app.route("/lights", methods=["GET"])
def lights():
    global light_status
    global led

    if light_status == False:
        led.on()
        light_status = True
    else:
        led.off()
        light_status = False
    
    return ('', 204)


#API CALL
@app.route("/query", methods=["GET"])
def query():

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
        cur.execute("SELECT * FROM thlog2 ORDER BY id DESC LIMIT 1")
        
        for (temperature, humidity, time, id) in cur:
            pass
        
        # Creating dictionary to send back in JSON form
        info = {"temperature":str(format(round(temperature, 2), '.2f')) + " °F",
            "humidity":str(format(round(humidity, 2), '.2f')) + " %",
            "time":time,
            "id":id
        }
    
    except mariadb.Error as e:
                print(f"Error: {e}")
    
    # Close Connection
    conn.close()

    return jsonify(info) # returning a JSON response

    
# table query
@app.route("/querytable")
def querytable():
        
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
            cur.execute("SELECT * FROM thlog2 ORDER BY id DESC LIMIT 30000")
            templogs = []
            datelogs = []
            
            k = 0
            for (temperature, humidity, time, id) in cur:
                k += 1
                if (k % 500 != 0):
                    continue
                
                templogs.append(format(round(temperature, 2), '.2f'))
                datelogs.append(time)
            templogs.reverse()
            datelogs.reverse()
            newlogs = [templogs, datelogs]
            print(newlogs)
        
        #     # Creating dictionary to send back in JSON form
        #     info = {"temperature":str(round(temperature, 2)) + " °F",
        #         "humidity":str(round(humidity, 2)) + " %",
        #         "time":time,
        #         "id":id
        #     }
        #     print(info)
        
        except mariadb.Error as e:
                    print(f"Error: {e}")
        
        # Close Connection
        conn.close()

        
        return jsonify(newlogs) # returning a JSON response


# table query
@app.route("/queryhumidity")
def queryhumidity():
        
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
            cur.execute("SELECT * FROM thlog2 ORDER BY id DESC LIMIT 30000")
            humiditylogs = []
            datelogs = []
            
            k = 0
            for (temperature, humidity, time, id) in cur:
                k += 1
                if (k % 500 != 0):
                    continue
                
                humiditylogs.append(format(round(humidity, 2), '.2f'))
                datelogs.append(time)

            humiditylogs.reverse()
            datelogs.reverse()
            newlogs = [humiditylogs, datelogs]
    
        
        except mariadb.Error as e:
                    print(f"Error: {e}")
        
        # Close Connection
        conn.close()

        
        return jsonify(newlogs) # returning a JSON response


def gen_frames():
    global camera
    while True:
        
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result



@app.route('/livestream')
def livestream():
    return render_template('livestream.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



# Raspberry Pi Internal Temperature
@app.route("/measuretemp")
def measure_temp():
        temp = os.popen("""vcgencmd measure_temp | awk -F "[=']" '{print($2 * 1.8)+32}'""").readline()
        print("inside measure temp")
        return jsonify(temp)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
   app.run( host='0.0.0.0', port=80)

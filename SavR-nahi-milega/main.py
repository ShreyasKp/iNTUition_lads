from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import pyrebase
import requests
import googlemaps
import gmaps
import webbrowser
import math
import geopy
from datetime import datetime
from geopy.geocoders import Nominatim

app = Flask(__name__)       #Initialze flask constructor

#Add your own details
config = {
  "apiKey": "AIzaSyAJJ3Kp9j5PSqttY_ldYQ4T_my4v_hQN34",
  "authDomain": "savr-nahi-milega.firebaseapp.com",
  "databaseURL": "https://savr-nahi-milega-default-rtdb.firebaseio.com/",
  "projectId": "savr-nahi-milega",
  "storageBucket": "savr-nahi-milega.appspot.com"
}

#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
db1 = firebase.database()
db2 = firebase.database()

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": "", "usertype": "", "add1": "", "add2": "", "pincode": ""}
rest = {"rest_id": "", "weight": "", "no_packets": "", "cuisine": ""}
buyer = {"buyer_id": "", "rest_name": "", "cuisine": ""}
rest_id = "onPEAUuSRTeo5LnphUcrcjOU20j1"
buyer_id = "zb2opGtKYYNBHcExjc5BGCDne4t1"

def convertTuple(tup):
    stri = ''
    stri = ','.join(tup)
    return stri

def index_to_go(s):
    return sorted(range(len(s)), key=lambda k: s[k])[0]

#Login
@app.route("/")
def login():
    return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
    return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"], name = person["name"], usertype = person["usertype"], add1 = person["add1"], add2 = person["add2"], pincode = person["pincode"])
    else:
        return redirect(url_for('login'))

@app.route("/restaurant")
def restaurant():
    if person["is_logged_in"] == True:
        global rest_id
        rest_id = person["uid"]
        return render_template("rest_add.html")
    else:
        return redirect(url_for('login'))

@app.route("/buyer")
def buyer():
    if person["is_logged_in"] == True:
        global buyer_id
        buyer_id = person["uid"]
        return render_template("buyer_add.html")
    else:
        return redirect(url_for('login'))

@app.route("/volunteer")
def volunteer():
    if person["is_logged_in"] == True:
        return render_template("volunteer.html", email = person["email"], name = person["name"], usertype = person["usertype"], add1 = person["add1"], add2 = person["add2"], pincode = person["pincode"])
    else:
        return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ["POST", "GET"])
def result():
    if request.method == "POST":        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:
            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            person["usertype"] = data.val()[person["uid"]]["usertype"]
            person["add1"] = data.val()[person["uid"]]["add1"]
            person["add2"] = data.val()[person["uid"]]["add2"]
            person["pincode"] = data.val()[person["uid"]]["pincode"]
            #Redirect to user profile page
            if person["usertype"] == 'Restaurant':
                return redirect(url_for('restaurant'))
            elif person["usertype"] == 'Volunteer':
                return redirect(url_for('volunteer'))
            elif person["usertype"] == 'Buyer':
                return redirect(url_for('buyer'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        email = result["email"]
        password = result["pass"]
        usertype = result["usertype"]
        add1 = result["add1"]
        add2 = result["add2"]
        pincode = result["pincode"]
        name = result["name"]
        try:
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            person["usertype"] = usertype
            person["add1"] = add1
            person["add2"] = add2
            person["pincode"] = pincode
            #Append data to the firebase realtime database
            data = {"name": name, "email": email, "usertype": usertype, "add1": add1, "add2": add2, "pincode": pincode}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            #return redirect(url_for('welcome'))
            #Redirect to user profile page
            if person["usertype"] == 'Restaurant':
                return redirect(url_for('restaurant'))
            elif person["usertype"] == 'Volunteer':
                return redirect(url_for('volunteer'))
            elif person["usertype"] == 'Buyer':
                return redirect(url_for('buyer'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

#If a restaurant logs in, they are redirected to /publish
@app.route("/publish", methods = ["POST", "GET"])
def publish():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        weight = result["weight"]
        no_packets = result["no_packets"]
        cuisine = result["cuisine"]
        try:
            #Add data to global restaurant
            global rest
            rest["rest_id"] = rest_id
            rest["weight"] = weight
            rest["no_packets"] = no_packets
            rest["cuisine"] = cuisine
            #Append data to the firebase realtime database
            rest_data = {"rest_id": rest_id, "weight": weight, "no_packets": no_packets, "cuisine": cuisine}
            # rest_data = {"weight": weight, "no_packets": no_packets, "cuisine": cuisine}
            db1.child("restaurant").child(rest["rest_id"]).set(rest_data)
            #Go to notification page <TODO: Write Please wait a volunteer is on his way>
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('publish'))

    """
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))
    """

#If a buyer logs in, they are redirected to /buy
@app.route("/buy", methods = ["POST", "GET"])
def buy():
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        restname = result["restname"]
        cuisine = result["cuisine"]
        print('Debug point 1')
        print(buyer_id)
        print(restname)
        print(cuisine)
        try:
            #Add data to global restaurant
            # global buyer
            # buyer["buyer_id"] = buyer_id
            # buyer["restname"] = restname
            # buyer["cuisine"] = cuisine
            # print('buyer: ', buyer)
            #Append data to the firebase realtime database
            buyer_data = {"buyer_id": buyer_id, "restname": restname, "cuisine": cuisine}
            db2.child("buyer").child(buyer_id).set(buyer_data)
            print('buyer_data: ', buyer_data)
            #Go to notification page <TODO: Write Please wait a volunteer is on his way>
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('buy'))

#If a volunteer logs in, they are redirected to /map
@app.route("/map", methods = ["GET"])
def map():
    if request.method == "GET":        #Only listen to POST
        # result = request.form           #Get the data submitted
        # rest_name = result["rest_name"]
        # cuisine = result["cuisine"]
        try:
            restaurants = db1.child("restaurant").get()
            """
            person["name"] = restaurants.val()[person["uid"]]["name"]
            person["usertype"] = data.val()[person["uid"]]["usertype"]
            person["add1"] = data.val()[person["uid"]]["add1"]
            person["add2"] = data.val()[person["uid"]]["add2"]
            person["pincode"] = data.val()[person["uid"]]["pincode"]
            buyer["rest_name"] = rest_name
            buyer["cuisine"] = cuisine
            #Append data to the firebase realtime database
            buyer_data = {"buyer_id": buyer_id, "rest_name": rest_name, "cuisine": cuisine}
            db.child("buyer").child(buyer["buyer_id"]).set(buyer_data)
            #Go to notification page <TODO: Write Please wait a volunteer is on his way>
            return redirect(url_for('welcome'))
            """
            print(restaurants)
        except:
            #If there is any error, redirect to register
            return redirect(url_for('map'))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
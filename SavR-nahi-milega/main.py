from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import pyrebase

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

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": "", "usertype": "", "add1": "", "add2": "", "pincode": ""}
restaurant = {"rest_id": "", "weight": "", "no_packets": "", "cuisine": ""}
buyer = {"buyer_id": "", "rest_name": "", "cuisine": ""}

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
            #Redirect to welcome page
            return redirect(url_for('welcome'))
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
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))

#If a restaurant logs in, they are redirected to /publish
@app.route("/publish/<rest_id>", methods = ["POST", "GET"])
def publish(rest_id):
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        weight = result["weight"]
        no_packets = result["no_packets"]
        cuisine = result["cuisine"]
        try:
            #Add data to global restaurant
            global restaurant
            restaurant["weight"] = weight
            restaurant["no_packets"] = no_packets
            restaurant["cuisine"] = cuisine
            #Append data to the firebase realtime database
            rest_data = {"rest_id": rest_id, "weight": weight, "no_packets": no_packets, "cuisine": cuisine}
            db.child("restaurant").child(restaurant["rest_id"]).set(rest_data)
            #Go to notification page <TODO: Write Please wait a volunteer is on his way>
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('publish/<rest_id>'))

    """
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))
    """

#If a buyer logs in, they are redirected to /buy
@app.route("/buy/<buyer_id>", methods = ["POST", "GET"])
def buy(buyer_id):
    if request.method == "POST":        #Only listen to POST
        result = request.form           #Get the data submitted
        rest_name = result["rest_name"]
        cuisine = result["cuisine"]
        try:
            #Add data to global restaurant
            global buyer
            buyer["rest_name"] = rest_name
            buyer["cuisine"] = cuisine
            #Append data to the firebase realtime database
            buyer_data = {"buyer_id": buyer_id, "rest_name": rest_name, "cuisine": cuisine}
            db.child("buyer").child(buyer["buyer_id"]).set(buyer_data)
            #Go to notification page <TODO: Write Please wait a volunteer is on his way>
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('publish/<rest_id>'))

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
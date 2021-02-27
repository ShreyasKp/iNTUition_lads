import pyrebase
from flask import *
app = Flask(__name__)
config = {
    "apiKey": "AIzaSyAJJ3Kp9j5PSqttY_ldYQ4T_my4v_hQN34",
    "authDomain": "savr-nahi-milega.firebaseapp.com",
    "databaseURL": "https://savr-nahi-milega.firebaseio.com",
    "projectId": "savr-nahi-milega",
    "storageBucket": "savr-nahi-milega.appspot.com",
    "messagingSenderId": "439412640461",
    "appId": "1:439412640461:web:340c5094eaeba28f887784",
    "measurementId": "G-YD0GR1VWWE"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])

def basic():
	unsuccessful = 'Please check your credentials'
	successful = 'Login successful'
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['pass']
		try:
			auth.sign_in_with_email_and_password(email, password)
			return render_template('new.html', s=successful)
		except:
			return render_template('new.html', us=unsuccessful)

	return render_template('new.html')


if __name__ == '__main__':
	app.run()

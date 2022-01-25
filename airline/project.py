from flask import Flask, render_template, redirect, url_for, request, session
import mysql.connector
from flaskext.mysql import MySQL
import random

app = Flask(__name__)
mysql = MySQL()
app.secret_key = 'key'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MyNewPassword1#'
app.config['MYSQL_DATABASE_DB'] = 'flight_reservation'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor =conn.cursor()

def seating_options(flight_num):
	query = "SELECT seat_num FROM seat WHERE \
			(flight_num = (%s)) AND (is_booked = 0)"
	cursor.execute(query, (flight_num,))
	results = cursor.fetchall()
	return [i[0] for i in results]

def add_seat(seat_num):
	query = "INSERT INTO seat_in_flight(seat_num, flight_num, customer_id) VALUES(%s, %s, %s)"
	cursor.execute(query, (seat_num, session['flight_num'], session['customer_id'],))
	conn.commit()

def show_statistics():
	query = "SELECT busy_pilot(), loyal_customer(), popular_dest()"
	cursor.execute(query)
	result = cursor.fetchall()
	return result[0][0], result[0][1], result[0][2]

def show_trips(c_id):
	query  = "SELECT * FROM show_trips where customer_id = (%s)"
	cursor.execute(query, (c_id,))
	result = cursor.fetchall()
	return result

def add_flight(flight_num, plane_type, airline, depart_airport, arrive_airport, depart_gate, arrive_gate):
	query = "CALL add_flight(%s, %s, %s, %s, %s, %s, %s)"
	cursor.execute(query, (flight_num, plane_type, airline, depart_airport, arrive_airport, depart_gate, arrive_gate,))
	conn.commit()

def add_pilot(pilot_num, pilot_name, airline, address, city, state, zip, phone_number, gender, date_of_birth, age):
	query = "CALL add_pilot(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	cursor.execute(query, (pilot_num, pilot_name, airline, gender, address, city, state, zip, date_of_birth, age, phone_number))
	conn.commit()

def add_entry(customer_id, customer_name, phone_number, address, city, state, zip,gender, date_of_birth, age):
	query = "CALL add_customer(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
	cursor.execute(query, (customer_id, customer_name, gender, address, city, state, zip, date_of_birth, age, phone_number))
	conn.commit()

def remove_flight(flight_num):
    query = "DELETE FROM flight where flight_num = (%s)"
    cursor.execute(query, (flight_num,))
    conn.commit()


def show_jobs(pilot_num):
	query = "SELECT * FROM show_jobs \
				WHERE pilot_num = (%s)"
	cursor.execute(query, (pilot_num,))
	results = cursor.fetchall()
	return results

def validate_user(c_id, customer_name):
	query = "SELECT customer_name FROM customer where customer_id = (%s)"
	cursor.execute(query, (c_id))
	result = cursor.fetchall()
	if result:
		return True
	else:
		return False

def validate_pilot(pilot_num, pilot_name):
	query = "SELECT pilot_name FROM pilot where pilot_num = (%s)"
	cursor.execute(query, (pilot_num))
	result = cursor.fetchall()
	if result:
		return True
	else:
		return False

def show_options():
	query = "SELECT flight_num, depart_airport, arrive_airport FROM show_options WHERE \
			(is_full != 1 and has_pilot!=0)"
	cursor.execute(query)
	result = cursor.fetchall()
	return result

def show_options_pilot():
	query = "SELECT flight_num, depart_airport, arrive_airport FROM show_options WHERE has_pilot!=1"
	cursor.execute(query)
	result = cursor.fetchall()
	return result

def enter_trip(depart_airport, arriv_airport, customer_id, flight_num, trip_id, seat_num):
	print(depart_airport, arriv_airport, customer_id, flight_num, trip_id, seat_num)
	query = "CALL add_trip(%s, %s, %s, %s, %s, %s)"
	cursor.execute(query, (depart_airport, arriv_airport, customer_id, flight_num, trip_id, seat_num))
	conn.commit()

def enter_job(pilot_num, flight_num):
	query = "CALL add_job(%s, %s)"
	cursor.execute(query, (pilot_num, flight_num,))
	conn.commit()

def validate_admin(admin_id, password):
	if admin_id == 1234 and password == 1111:
		return True
	else:
		return False

@app.route('/newpilot', methods=['GET', 'POST'])
def newpilot():
	if request.method == 'POST':
		pilot_num = request.form.get('pilot_num', '')
		pilot_name = request.form.get('pilot_name', '')
		airline = request.form.get('airline', '')
		address = request.form.get('address','')
		city = request.form.get('city','')
		state = request.form.get('state','')
		zip = request.form.get('zip','')
		phone_number = request.form.get('phone_number','')
		gender = request.form.get('gender','')
		date_of_birth = request.form.get('date_of_birth','')
		age = request.form.get('age','')
		add_pilot(pilot_num, pilot_name, airline, address, city, state, zip, phone_number, gender, date_of_birth, age)
		return render_template('home_admin.html')
	return render_template('newpilot.html')

@app.route('/newflight', methods=['GET', 'POST'])
def newflight():
	if request.method == 'POST':
		flight_num = request.form.get('flight_num','')
		plane_type = request.form.get('plane_type','')
		airline = request.form.get('airline','')
		depart_airport = request.form.get('depart_airport','')
		arrive_airport = request.form.get('arrive_airport','')
		depart_gate = request.form.get('depart_gate','')
		arrive_gate = request.form.get('arrive_gate','')
		add_flight(flight_num, plane_type, airline, depart_airport, arrive_airport, depart_gate, arrive_gate)
		return render_template('home_admin.html')
	
	else:
		return render_template('newflight.html')

@app.route('/showcurrentflights', methods=['GET'])
def showcurrentflights():
	options = show_options_pilot()
	return render_template('showcurrentflights.html', options = options, length=len(options))


@app.route('/')
def main_page():
	return render_template('mainpage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		'''
		A form has been submitted. Redirect to logged in user page.
		'''
		customer_id = request.form.get('customer_id')
		customer_name = request.form.get('customer_name')
		if validate_user(customer_id, customer_name):
			#add session variables
			session['customer_id'] = customer_id
			session['customer_name'] = customer_name
			return redirect(url_for('user'))
		else:
			return render_template('login.html')
	else:
		'''
		Display login page
		'''
		return render_template('login.html')

@app.route('/loginpilot', methods=['GET', 'POST'])
def loginpilot():
	if request.method == 'POST':
		'''
		A form has been submitted. Redirect to logged in user page.
		'''
		pilot_num = request.form['pilot_num']
		pilot_name = request.form['pilot_name']
		if validate_pilot(pilot_num, pilot_name):
			#add session variables
			session['pilot_num'] = pilot_num
			session['pilot_name'] = pilot_name
			return redirect(url_for('pilot'))
		else:
			return render_template('loginpilot.html')
	else:
		'''
		Display login page
		'''
		return render_template('loginpilot.html')

@app.route('/deleteflight', methods=['GET', 'POST'])
def deleteflight():
	if request.method == 'POST':
		flight_num = request.form['flight_num']
		remove_flight(int(flight_num))
		return render_template('home_admin.html')
	else:
		options = show_options_pilot()
		return render_template('deleteflight.html', options = options, length=len(options))


@app.route('/statistics', methods=['GET', 'POST'])
def statistics():
	busy_pilot, loyal_customer, popular_dest = show_statistics()
	return render_template('stat.html', busy_pilot=busy_pilot, \
						loyal_customer=loyal_customer, popular_dest=popular_dest)

@app.route('/admin')
def admin():
	if 'admin_id' in session:
		return render_template('home_admin.html')
	else:
		return redirect(url_for('loginadmin'))

@app.route('/loginadmin', methods=['GET', 'POST'])
def loginadmin():
	if request.method == 'POST':
		'''
		A form has been submitted. Redirect to logged in user page.
		'''
		admin_id = request.form['admin_id']
		password = request.form['password']
		if validate_admin(int(admin_id), int(password)):
			session['admin_id'] = admin_id
			return redirect(url_for('admin'))
		else:
			return render_template('loginadmin.html')
	else:
		'''
		Display login page
		'''
		return render_template('loginadmin.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		customer_id = request.form.get('customer_id','')
		customer_name = request.form.get('customer_name','')
		phone_number = request.form.get('phone_num','')
		address = request.form.get('address','')
		city = request.form.get('city','')
		state = request.form.get('state','')
		zip = request.form.get('zip','')
		gender = request.form.get('gender','')
		date_of_birth = request.form.get('date_of_birth','')
		age = request.form.get('age','')
		add_entry(customer_id, customer_name, phone_number, address, city, state, zip,gender, date_of_birth, age)
		return render_template('mainpage.html')
	else:
		return render_template('signup.html')

@app.route('/jobs')
def jobs():
	pilot_num = session['pilot_num']
	results = show_jobs(pilot_num)
	return render_template('pilotjobs.html', results=results, length=len(results))

@app.route('/pilot', methods=['GET', 'POST'])
def pilot():
	if 'pilot_num' in session:
		return render_template('home_pilot.html')
	else:
		return redirect(url_for('loginpilot'))

@app.route('/user', methods=['GET', 'POST'])
def user():
	if 'customer_id' in session:
		return render_template('home_customer.html')
	else:
		return redirect(url_for('login'))

@app.route('/trips')
def trip():
	c_id = session['customer_id']
	results = show_trips(c_id)
	return render_template('trips.html', trips=results, length=len(results))


@app.route('/logout')
def logout():
	session.pop('customer_id', None)
	return redirect(url_for('main_page'))

@app.route('/logoutpilot')
def logoutpilot():
	session.pop('pilot_num', None)
	return redirect(url_for('main_page'))

@app.route('/logoutadmin')
def logoutadmin():
	session.pop('admin_id', None)
	return redirect(url_for('main_page'))

@app.route('/pilotnewjob', methods=['GET', 'POST'])
def book_job():
	if request.method == 'POST':
		options = show_options_pilot()
		idx = request.form['i']
		flight_num = options[int(idx)][0]
		pilot_num = session['pilot_num']
		enter_job(pilot_num, flight_num)
		return render_template('booking_done_pilot.html')
	elif 'pilot_num' in session:
		options = show_options_pilot()
		return render_template('book_job.html', options = options, length=len(options))
	else:
		return redirect(url_for('loginpilot'))


@app.route('/book_seat', methods=['GET', 'POST'])
def book_seat():
	if request.method == 'POST':
		seat_num = request.form['i']
		depart_airport = session['depart_airport']
		arriv_airport = session['arriv_airport']
		customer_id = session['customer_id']
		flight_num = session['flight_num']
		trip_id = session['trip_id']
		enter_trip(depart_airport, arriv_airport, customer_id, flight_num, trip_id, seat_num)
		return render_template('booking_done.html', flight=session['flight_num'], \
								depart=session['depart_airport'], arr=session['arriv_airport'], \
								c_id=session['customer_id'])
	elif 'flight_num' in session:
		seating_options_available = seating_options(session['flight_num'])
		print('seating: ', session['flight_num'],seating_options_available)
		return render_template('book_seat.html', seating_options_available = seating_options_available,depart_airport=session['depart_airport'], arriv_airport=session['arriv_airport'], \
								flight_num=session['flight_num'], trip_id=session['trip_id'], customer_id=session['customer_id'])
	else:
		return redirect(url_for('logout'))


@app.route('/book', methods=['GET', 'POST'])
def book_flight():
	if request.method == 'POST':
		options = show_options()
		idx = request.form['i']
		depart_airport = options[int(idx)][1]
		flight_num = options[int(idx)][0]
		arriv_airport  =options[int(idx)][2]
		customer_id = session['customer_id'] 
		session['arriv_airport'] = arriv_airport
		session['depart_airport'] = depart_airport
		trip_id = str(random.randint(1e2, 1e4)) + str(random.randint(1e4, 1e6))
		session['trip_id'] = trip_id
		session['flight_num'] = flight_num
		return redirect(url_for('book_seat', \
								depart_airport=depart_airport, arriv_airport=arriv_airport, \
								flight_num=flight_num, trip_id=trip_id, customer_id=customer_id))
	elif 'customer_id' in session:
		options = show_options()
		return render_template('book.html', options = options, length=len(options))
	else:
		return redirect(url_for('login'))

app.run(debug=True, port=5100)
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import bcrypt
import requests
import os
import logging

# Initialize Flask app
app = Flask(__name__)

# Configuration class
class Config:
    SECRET_KEY = os.getenv('awhikhafhakfjajfoaufaifiahfiahfaifia')
    

    # MySQL Configuration
    MYSQL_HOST = os.getenv('MYSQL_HOST', '213.48.243.107')
    MYSQL_USER = os.getenv('MYSQL_USER', 'idrac')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'h)iqAThfRSZ5PR!K')
    MYSQL_DB = os.getenv('MYSQL_DB', 'idrac_panel')

    # iDRAC Configuration
    IDRAC_IP = os.getenv('IDRAC_IP', '192.168.10.111')
    IDRAC_USER = os.getenv('IDRAC_USER', 'root')
    IDRAC_PASSWORD = os.getenv('IDRAC_PASSWORD', 'admin1')
    IDRAC_BASE_URL = f'https://{IDRAC_IP}/redfish/v1'

    # Session security
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

# Apply configuration
app.config.from_object(Config)

# Initialize MySQL
mysql = MySQL(app)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to make authenticated requests to iDRAC
def make_idrac_request(endpoint, method='GET', data=None):
    url = f'{Config.IDRAC_BASE_URL}{endpoint}'
    headers = {'Content-Type': 'application/json'}
    auth = (Config.IDRAC_USER, Config.IDRAC_PASSWORD)

    try:
        response = requests.request(method, url, headers=headers, auth=auth, json=data, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"iDRAC API request failed: {e}")
        return {'error': str(e)}

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Fetch user from database
        try:
            with mysql.connection.cursor() as cur:
                cur.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cur.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Invalid username or password')
        except Exception as e:
            logger.error(f"Database error: {e}")
            return render_template('login.html', error='An error occurred. Please try again.')

    return render_template('login.html')

# Dashboard route (iDRAC panel)
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Route to fetch system information
@app.route('/system-info')
def system_info():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    system_info = make_idrac_request('/Systems/System.Embedded.1')
    return jsonify(system_info)

# Route to fetch power status
@app.route('/power-status')
def power_status():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    power_status = make_idrac_request('/Chassis/System.Embedded.1/Power')
    return jsonify(power_status)

# Route to perform power action
@app.route('/power-action', methods=['POST'])
def power_action():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    action = request.json.get('action')
    if action not in ['On', 'Off', 'GracefulShutdown', 'ForceRestart']:
        return jsonify({'error': 'Invalid action'}), 400

    payload = {'ResetType': action}
    response = make_idrac_request('/Systems/System.Embedded.1/Actions/ComputerSystem.Reset', method='POST', data=payload)
    return jsonify(response)

# Run the application
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5007,

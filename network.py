from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import re

app = Flask(__name__)
app.secret_key = "awffafafafahfiahfiahihfaihfih"  # To enable flashing messages

# UniFi Controller details
controller_url = "https://192.168.0.1"  # Replace with your UniFi Controller URL
api_key = "5lTzPdBe725ogEaMtI1bJ00pZKo9DDl0"  # Replace with your API key

# Disable SSL warnings (for testing only)
requests.packages.urllib3.disable_warnings()

# Step 1: Set up headers with the API key for authentication
headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json"
}

# API URL to verify email
email_verification_url = "https://store.swiftpeakhosting.co.uk/admin/api-v1/verify-email"  # Adjust URL based on your API

# Function to verify email via API
def verify_email(email):
    response = requests.post(email_verification_url, json={"email": email}, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            return True  # Email is verified
        else:
            return False  # Email is not verified
    return False  # Error in API request

# Function to validate the local IP address
def validate_local_ip(local_ip):
    # Check if IP starts with '192.168.'
    return local_ip.startswith("192.168.")

@app.route('/')
def index():
    return render_template('index.html')  # Your HTML page

@app.route('/verify_email', methods=['POST'])
def verify_email_route():
    email = request.form['email']
    local_ip = request.form['local_ip']
    
    # Provide guidance to the user for obtaining their local IP
    flash("To find your local IP address, follow these steps:", "info")
    flash("On Windows: Open Command Prompt and run 'ipconfig'. Look for 'IPv4 Address' starting with 192.168.", "info")
    flash("On Linux: Open Terminal and run 'ip a'. Look for the IP address starting with 192.168.", "info")
    
    # Step 1: Verify email
    if not verify_email(email):
        flash(f"Email {email} is not verified or not registered. Please check and try again.", "danger")
        return redirect(url_for('index'))  # Return to form if verification fails
    
    # Step 2: Validate local IP
    if not validate_local_ip(local_ip):
        flash(f"The IP address {local_ip} is not valid. It should start with '192.168.'", "danger")
        return redirect(url_for('index'))  # Return to form if IP validation fails

    flash(f"Email {email} and IP {local_ip} are verified. Proceeding with port forwarding.", "success")
    return redirect(url_for('apply_port_forward'))  # Redirect to apply port forwarding

@app.route('/apply_port_forward', methods=['GET', 'POST'])
def apply_port_forward():
    if request.method == 'POST':
        # Get form data
        dst_port = request.form['dst_port']
        fwd_ip = request.form['fwd_ip']
        fwd_port = request.form['fwd_port']
        protocol = request.form['protocol']
        name = request.form['name']

        # Step 3: Apply the port forwarding rule
        port_forward_rule = {
            "enabled": True,
            "name": name,
            "src": "any",  # Source (any or specific IP)
            "src_port": "any",  # Source port (any or specific port)
            "dst_port": dst_port,  # External port
            "fwd_ip": fwd_ip,  # Internal IP address
            "fwd_port": fwd_port,  # Internal port
            "protocol": protocol,  # Protocol (tcp, udp, or tcp_udp)
            "log": False  # Enable logging (optional)
        }

        rules_url = f"{controller_url}/api/s/default/rest/firewallrule"
        response = requests.post(rules_url, json=port_forward_rule, headers=headers, verify=False)
        if response.status_code == 200:
            flash(f"Port forwarding rule for {dst_port} created successfully!", "success")
            return redirect(url_for('index'))  # Redirect back to the form
        else:
            flash(f"Failed to create port forwarding rule: {response.text}", "danger")
            return redirect(url_for('index'))

    return render_template('port_forward_form.html')  # Template for the port forwarding form

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=6001)

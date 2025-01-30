from flask import Flask, render_template
import threading
import time
import requests

app = Flask(__name__)

# List of websites to monitor
websites = [
    "https://store.swiftpeakhosting.co.uk",
    "https://",
    "https://www.stackoverflow.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.reddit.com",
    "https://www.facebook.com",
    "https://www.twitter.com",
    "https://www.microsoft.com",
    "https://www.apple.com"
]

# Dictionary to store website statuses
statuses = {website: "Unknown" for website in websites}

# Function to check website status
def check_status():
    while True:
        for website in websites:
            try:
                response = requests.get(website, timeout=5)
                statuses[website] = "Online" if response.status_code == 200 else "Offline"
            except requests.exceptions.RequestException:
                statuses[website] = "Offline"
        time.sleep(30)

# Route for the status page
@app.route("/")
def status_page():
    return render_template("status.html", statuses=statuses)

# Start the background thread for status checking
threading.Thread(target=check_status, daemon=True).start()

if __name__ == "__main__":
    app.run(debug=True, port=5001)

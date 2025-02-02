from flask import Flask, request, render_template, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = "afwafwawfaffwy"  # Required for session handling

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1333569010272309258/zF_dD8J88pDoZ2OKLEc-Kd4WMfsTJGBrsqGZ_ys73MQOKRUcieCUWLl1FzTSgV8z9CEZ"

@app.route("/", methods=["GET"])
def show_form():
    """ Show the HTML form on GET requests """
    return render_template("form.html")

@app.route("/", methods=["POST"])
def handle_form():
    """ Handle form submission and send data to Discord """
    try:
        print("Received POST request")

        # Get request data (JSON or Form)
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()

        print("Received Data:", data)  # Debugging

        user_email = data.get("user_email")
        cad_domain = data.get("cad_domain")
        api_domain = data.get("api_domain")
        cloudflare_code = data.get("cloudflare_code")

        if not all([user_email, cad_domain, api_domain, cloudflare_code]):
            print("Error: Missing fields")
            return jsonify({"error": "All fields are required."}), 400

        # Format Webhook Message
        payload = {
            "content": (
                f"**User Email:** {user_email}\n"
                f"**CAD Domain:** {cad_domain}\n"
                f"**API Domain:** {api_domain}\n"
                f"**Cloudflare Tunnel Code:**\n```\n{cloudflare_code}\n```"
            )
        }

        print("Sending payload to Discord:", payload)

        # Send data to Discord Webhook
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print("Discord Response Code:", response.status_code)

        if response.status_code == 204:
            return jsonify({"message": "Information sent successfully!"}), 200
        else:
            return jsonify({"error": f"Failed to send. Error: {response.status_code}, {response.text}"}), 500

    except Exception as e:
        print("Server Error:", str(e))
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5003)

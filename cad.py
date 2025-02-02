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
    if session.get("form_submitted"):
        return jsonify({"message": "You have already submitted the form."}), 400  # Prevent resubmission

    try:
        data = request.get_json() or request.form.to_dict()
        user_email = data.get("user_email")
        cad_domain = data.get("cad_domain")
        api_domain = data.get("api_domain")
        cloudflare_code = data.get("cloudflare_code")

        if not all([user_email, cad_domain, api_domain, cloudflare_code]):
            return jsonify({"error": "All fields are required."}), 400  # Send error as JSON

        # Format Webhook Message
        payload = {
            "content": (
                f"**User Email:** {user_email}\n"
                f"**CAD Domain:** {cad_domain}\n"
                f"**API Domain:** {api_domain}\n"
                f"**Cloudflare Tunnel Code:**\n```\n{cloudflare_code}\n```"
            )
        }

        # Send data to Discord Webhook
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

        if response.status_code == 204:
            session["form_submitted"] = True  # Mark form as submitted
            return jsonify({"message": "Information sent successfully!"}), 200
        else:
            return jsonify({"error": f"Failed to send. Error: {response.status_code}"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return JSON error message

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5003)

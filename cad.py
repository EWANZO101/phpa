from flask import Flask, request, render_template, session
import requests

app = Flask(__name__)
app.secret_key = "afwafwawfaffwy"  # Required for session handling

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1333569010272309258/zF_dD8J88pDoZ2OKLEc-Kd4WMfsTJGBrsqGZ_ys73MQOKRUcieCUWLl1FzTSgV8z9CEZ"

@app.route("/", methods=["GET", "POST"])
def handle_form():
    message = None  # Default message

    # Debugging: Clear session manually for testing
    session.pop("form_submitted", None)

    if session.get("form_submitted"):
        message = "You have already submitted the form."
        return render_template("form.html", message=message)

    if request.method == "POST":
        try:
            # Handle both JSON and form submissions
            data = request.get_json() or request.form

            user_email = data.get("user_email")
            cad_domain = data.get("cad_domain")
            api_domain = data.get("api_domain")
            cloudflare_code = data.get("cloudflare_code")

            # Validate required fields
            if not all([user_email, cad_domain, api_domain, cloudflare_code]):
                return "All fields are required.", 400

            # Format the message
            payload = {
                "content": (
                    f"**User Email:** {user_email}\n"
                    f"**CAD Domain:** {cad_domain}\n"
                    f"**API Domain:** {api_domain}\n"
                    f"**Cloudflare Tunnel Code:**\n```\n{cloudflare_code}\n```"
                )
            }

            # Debugging: Print payload before sending
            print("Sending payload to Discord:", payload)

            # Send the message to the Discord webhook
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

            # Debugging: Print response details
            print("Response Code:", response.status_code)
            print("Response Text:", response.text)

            if response.status_code == 204:  # 204 means success in Discord webhooks
                message = "Information sent successfully!"
                session["form_submitted"] = True  # Mark the form as submitted
            else:
                message = f"Failed to send information. Error code: {response.status_code} - {response.text}"

        except Exception as e:
            message = f"An error occurred: {str(e)}"
            print("Error:", e)  # Print error to console for debugging

    return render_template("form.html", message=message)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5003)

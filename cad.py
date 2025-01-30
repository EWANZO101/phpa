from flask import Flask, request, render_template, session
import requests

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session handling

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1333569010272309258/zF_dD8J88pDoZ2OKLEc-Kd4WMfsTJGBrsqGZ_ys73MQOKRUcieCUWLl1FzTSgV8z9CEZ"

@app.route("/", methods=["GET", "POST"])
def handle_form():
    message = None  # Default message

    # Check if the user has already submitted the form
    if session.get("form_submitted"):
        message = "You have already submitted the form."
        return render_template("form.html", message=message)

    if request.method == "POST":
        try:
            # Parse JSON payload
            data = request.get_json()
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

            # Send the message to the Discord webhook
            response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

            # Check if the request was successful
            if response.status_code == 204:  # 204 is Discord's success code for webhooks
                message = "Information sent successfully!"
                session["form_submitted"] = True  # Mark the form as submitted
            else:
                message = f"Failed to send information. Error code: {response.status_code}"

        except Exception as e:
            message = f"An error occurred: {str(e)}"

    # Render the form with a message
    return render_template("form.html", message=message)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5003)

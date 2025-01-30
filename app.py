from flask import Flask, request, jsonify, render_template
import dns.resolver
import requests

app = Flask(__name__)

def check_cloudflare(domain):
    try:
        # DNS Lookup for NS Records
        answers = dns.resolver.resolve(domain, 'NS')
        for rdata in answers:
            if 'cloudflare.com' in str(rdata):
                return True  # Cloudflare nameservers detected

        # HTTP Headers Check
        response = requests.get(f"http://{domain}", timeout=5)
        headers = response.headers
        if any(key.lower().startswith('cf-') or 'cloudflare' in headers.get('Server', '').lower() for key in headers):
            return True  # Cloudflare headers detected
    except Exception as e:
        print(f"Error: {e}")
    return False  # Not using Cloudflare

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-cloudflare', methods=['POST'])
def check_cloudflare_route():
    data = request.json
    domain = data.get('domain')
    if not domain:
        return jsonify({'error': 'Domain is required'}), 400

    is_cloudflare = check_cloudflare(domain)
    return jsonify({'domain': domain, 'isCloudflare': is_cloudflare})
app.run(host="0.0.0.0", port=5000, debug=True)


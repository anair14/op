"""
Author: Ashwin Nair
Date: 2025-03-06
Project name: osint.py
Summary: Enter summary here.
"""

import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# def domain_lookup(domain):
#     try:
#         w = whois.whois(domain)
#         return w.text
#     except Exception as e:
#         return f"Error {e}"


def email_breach_check(email):
    api_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {"User-Agent": "OSINT-TOOL"}
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            return response.json()  # Return the breached data if available
        elif response.status_code == 404:  # No breaches found
            return "No breaches found."
        else:
            return f"Error: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def ip_geolocation(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        return response.json()
    except Exception as e:
        return f"Error: {e}"

def social_media_scraper(username):
    social_sites = [
        "https://twitter.com/{}",
        "https://www.instagram.com/{}",
        "https://github.com/{}",
        "https://www.reddit.com/user/{}"
    ]
    found_profiles = {}
    for site in social_sites:
        url = site.format(username)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                found_profiles[site.split("//")[1].split("/")[0]] = url
        except Exception as e:
            pass
    return found_profiles

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json(silent=True)  # Avoids throwing an error if JSON is invalid
    if not isinstance(data, dict):  # Ensure data is a dictionary
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    result = {}
    if 'email' in data and data['email']:
        result['email'] = email_breach_check(data['email'])
    if 'ip' in data and data['ip']:
        result['ip'] = ip_geolocation(data['ip'])
    if 'username' in data and data['username']:
        result['social_media'] = social_media_scraper(data['username'])

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)


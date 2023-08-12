from flask import Flask, jsonify
from flask_cors import CORS 
import requests
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/cctv/<country_code>', methods=['GET'])
def get_cctv_ips(country_code):
    try:
        countries = ["US", "JP", "IT", "KR", "FR", "DE", "TW", "RU", "GB", "NL",]
                     # ... (rest of the countries)

        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:68.0) Gecko/20100101 Firefox/68.0"}

        country = country_code.upper()
        if country not in countries:
            return jsonify({"error": "Invalid country code"}), 400

        res = requests.get(f"http://www.insecam.org/en/bycountry/{country}", headers=headers)
        last_page = re.findall(r'pagenavigator\("\?page=", (\d+)', res.text)[0]

        ip_list = []
        for page in range(int(last_page)):
            res = requests.get(
                f"http://www.insecam.org/en/bycountry/{country}/?page={page}",
                headers=headers
            )
            find_ip = re.findall(r"http://\d+\.\d+\.\d+\.\d+(?::\d+)?", res.text)
            ip_list.extend(find_ip)

        return jsonify({"ip_addresses": ip_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

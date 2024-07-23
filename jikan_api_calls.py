from __future__ import print_function
import requests
import sys
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/data', methods=['GET'])
def get_mal_data():
    # Define the API endpoint URL
    username = request.args.get('query')
    url = 'https://api.jikan.moe/v4/users/' + username + '/statistics'

    print("fetching api data", file=sys.stderr)

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            posts = response.json()
            return jsonify(posts)
        else:
            print('Error:', response.status_code)
            return None
        
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')
    
if __name__ == '__main__':
    app.run(debug=True)
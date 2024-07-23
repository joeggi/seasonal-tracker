from __future__ import print_function
import requests
import sys
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from dateutil import parser

app = Flask(__name__)
CORS(app)

@app.route('/data', methods=['GET'])
def get_mal_data():
    # Define the API endpoint URL
    username = request.args.get('query')
    url = 'https://api.jikan.moe/v4/users/' + username + '/history'

    print(url, file=sys.stderr)

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            posts = response.json()
            posts['data'] = posts['data'][:5]
            posts['entry0'] = posts['data'][0]
            posts['entry0']['date'] = parser.parse(posts['entry0']['date']).strftime('%A, %B %d, %Y at %I:%M %p')
            posts['entry1'] = posts['data'][1]
            posts['entry1']['date'] = parser.parse(posts['entry1']['date']).strftime('%A, %B %d, %Y at %I:%M %p')
            posts['entry2'] = posts['data'][2]
            posts['entry2']['date'] = parser.parse(posts['entry2']['date']).strftime('%A, %B %d, %Y at %I:%M %p')
            posts["username"] = username
            print(posts, file=sys.stderr)
            return render_template('userdata.html', **posts)
        else:
            print('Error:', response.status_code)
            return None
        
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
@app.route('/')
def index():
    print("test", file=sys.stderr)
    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)
from __future__ import print_function
import requests
import sys
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from dateutil import parser

app = Flask(__name__)
CORS(app)

# @app.route('/userupdates', methods=['GET'])

@app.route('/data', methods=['GET'])
def get_mal_data():
    username = request.args.get('query')
    # page = request.args.get('page', default=1, type=int)
    # start = (page - 1) * 5
    # end = start + 3
    # Define the API endpoint URL
    url = 'https://api.jikan.moe/v4/users/' + username + '/userupdates'

    print(url, file=sys.stderr)

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            posts = response.json()
            data_slice = {'title': {}, 'eps_seen': {}, 'date': {}, 'status': {}, 'rating': {}}
            for i in range(0, 3):
                data_slice['status'][i] = posts['data']['anime'][i]['status']
                data_slice['rating'][i] = 0
                data_slice['title'][i] = posts['data']['anime'][i]['entry']['title']
                data_slice['eps_seen'][i] = posts['data']['anime'][i]['episodes_seen']
                data_slice['rating'][i] = posts['data']['anime'][i]['score']
                data_slice['date'][i] = parser.parse(posts['data']['anime'][i]['date']).strftime('%A, %B %d, %Y at %I:%M %p')
            return render_template('userdata.html', username=username, data_slice=data_slice)
        else:
            print('Error:', response.status_code)
            return None
        
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
@app.route('/next-button')
def next():
    page += 1
    get_mal_data()

@app.route('/prev-button')
def prev():
    page -= 1
    get_mal_data()

    
@app.route('/')
def index():
    print("test", file=sys.stderr)
    data = {'username': 'Default User'}
    return render_template('index.html', data=data)
    
if __name__ == '__main__':
    app.run(debug=True)
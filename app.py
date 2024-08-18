from __future__ import print_function
import requests
import sys
from flask import Flask, request, jsonify, send_from_directory, render_template, flash
from flask_cors import CORS
from dateutil import parser

app = Flask(__name__)
CORS(app)

# @app.route('/userupdates', methods=['GET'])

@app.route('/activity', methods=['GET'])
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
            print(posts, file=sys.stderr)

            if len(posts['data']) == 0:
                return render_template('index.html')
            caption = "Here is some recent activity from " + username + ":"

            data_slice = {'title': {}, 'eps_seen': {}, 'date': {}, 'status': {}, 'rating': {}, 'message': {}}
            for i in range(0, 3):
                data_slice['status'][i] = posts['data']['anime'][i]['status']
                data_slice['rating'][i] = 0
                data_slice['title'][i] = posts['data']['anime'][i]['entry']['title']
                data_slice['eps_seen'][i] = posts['data']['anime'][i]['episodes_seen']
                data_slice['rating'][i] = posts['data']['anime'][i]['score']
                data_slice['date'][i] = parser.parse(posts['data']['anime'][i]['date']).strftime('%A, %B %d, %Y at %I:%M %p')
                match posts['data']['anime'][i]['status']:
                    case 'Completed':
                        data_slice['message'][i] = ('Finished series ' + data_slice['title'][i] + ' on ' + data_slice['date'][i] + 
                            ' , rated series a ' + str(data_slice['rating'][i]) + '/10.')
                    case 'Plan to Watch':
                        data_slice['message'][i] = ('Added series ' + data_slice['title'][i] + ' as planned to watch on ' + data_slice['date'][i] + '.')
                    case 'Watching':
                        if data_slice['eps_seen'][i] == None:
                            data_slice['message'][i] = ('Watched an episode on ' + data_slice['date'][i] + 
                                ', series is of unknown length.')
                        else:
                            data_slice['message'][i] = ('Watched episode ' + str(data_slice['eps_seen'][i]) + ' on ' + data_slice['date'][i] + '.')
                    case 'Re-watching':
                        data_slice['message'][i] = ('Rewatched up through episode ' + str(data_slice['eps_seen'][i]) + ' on ' + data_slice['date'][i] + 
                            '. ' + username + ' rated series a ' + str(data_slice['rating'][i]) + '/10.')
                    case 'On-Hold':
                        data_slice['message'][i] = ('Placed series on hold on ' + data_slice['date'][i] + 
                            ' after watching through episode ' + str(data_slice['eps_seen'][i]) + '.')
                    case 'Dropped':
                        data_slice['message'][i] = ('Dropped series on ' + data_slice['date'][i] + 
                            ' after watching through episode ' + str(data_slice['eps_seen'][i]) + '.')
            
            return render_template('userdata.html', data_type='activity', username=username, data_slice=data_slice, caption=caption)
        else:
            print('Error:', response.status_code)
            return None
        
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
    
@app.route('/favorites')
def favorites():
    username = request.args.get('query')
    url = "https://api.jikan.moe/v4/users/" + username + "/favorites"
    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)
        caption = "Here are " + username + "'s favorites!"

        if response.status_code == 200:
            posts = response.json()
            print(posts, file=sys.stderr)

            if len(posts['data']) == 0:
                return render_template('index.html')
            
            data_slice = {'title': {}, 'year': {}, 'char': {}}

            for i in range(0, min(len(posts['data']['anime']), 10)):
                data_slice['title'][i] = posts['data']['anime'][i]['title']
                data_slice['year'][i] = posts['data']['anime'][i]['start_year']
            for i in range(0, min(len(posts['data']['characters']), 10)):
                data_slice['char'][i] = posts['data']['characters'][i]['name']


            if len(posts['data']['anime']) == 0:
                data_slice['title'][i] = "NA"
            if len(posts['data']['characters']) == 0:
                data_slice['char'][i] = username + " has no favorite characters.."
            return render_template('userdata.html', caption=caption, data_type='favorites', data_slice=data_slice, username=username)
        
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
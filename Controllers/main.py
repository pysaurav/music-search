"""All the routes to get query from ajax request from templates and responses are handled here.
"""
import os
import json
import secrets
from flask import Flask, render_template, request, jsonify
from Models.models import search_track, get_a_playlist, search_playlist, get_available_countries, send_cache_clear_request
import os 

secret_key = secrets.token_hex(16)
print(os.getcwd())
# template_dir = os.path.join('Views','templates')
app = Flask(__name__, template_folder= '../Views/templates', static_folder='../Views/static')
app.config['SECRET_KEY'] = secret_key


@app.route('/', methods=['GET', 'POST'])
def main():
    """ This is the route for the the homepage view of webapp.

    Returns:
        html: Returns the rendered html template
    """
    if request.method == 'POST':
        pass
    return render_template('main.html', countries=get_available_countries())


@app.route('/searchTrack', methods=['POST', 'GET'])
def search_track_route():
    """ Route which gets the track search query and pass it to models and returns the json data.

    Returns:
        json: List of dictionaries; each dictionary with details of a track
    """
    query = request.args.get('q')
    market = request.args.get('market')
    print(query, market)
    ret = search_track(query, market)
    return jsonify(ret)


@app.route('/getPlaylist', methods=['POST', 'GET'])
def get_playlist():
    """Route which gets the playlistId and pass it to models and returns the details of a playlist.

    Returns:
        json: List of dictionaries; each dictionary with details of a tracks in the playlist.
    """
    query = request.args.get('q')
    data = get_a_playlist(query)
    return jsonify(data)


@app.route('/searchPlaylist', methods=['POST', 'GET'])
def search_playlist_route():
    """Route which gets the playlist search query and pass it to models and returns the json data.

    Returns:
        json: List of dictionaries; each dictionary with details of a track
    """
    query = request.args.get('q')
    market = request.args.get('market')
    data = search_playlist(query, market)
    return jsonify(data)


@ app.route('/about', methods=['GET', 'POST'])
def about():
    """Route for about page for the webapp

    Returns:
        html: rendered html template for about page
    """
    return render_template('about.html')


@ app.route('/health', methods=['GET', 'POST'])
def health():
    """Route for checking health of the app

    Returns:
    """
    return jsonify('{"msg":"Healthy"}'), 200


@ app.route('/clearCache', methods=['GET'])
def clearCache():
    """Route for clearing cache

    """
    country = request.args.get('q')
    status = send_cache_clear_request(country)
    return jsonify(status), 200


if __name__ == '__main__':

    #Passing credentials as environment variables
    cred_path = os.path.join('config', 'credentials.json')
    if os.path.exists(cred_path):
        with open(cred_path) as f:
            creds = json.load(f)
        os.environ["CLIENT_ID"] = creds["CLIENT_ID"]
        os.environ["CLIENT_SECRET"] = creds["CLIENT_SECRET"]

    app.run(debug=True, host='0.0.0.0', port=80)
    #app.run(debug=True, host='127.0.0.1', port=5000)

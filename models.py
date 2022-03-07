""" Data source for the webapp; All the interactions between spotifyAPI and
    queries from view.
"""
import json
import os
import requests
# pylint: disable= W0702, R0123, E0401, C0103
# Disabling exception type,literal comparison, f string formatter


def renew_auth_token(credentials):
    """Renews the authentication token of spotify and stores it to config/token.

    Args:
        credentials (dict): contains client_id and client_secret for spotify authentication

    Returns:
        string: authentication token
    """
    try:
        grant_type = 'client_credentials'
        body_params = {'grant_type': grant_type}

        url = 'https://accounts.spotify.com/api/token'
        response = requests.post(url, data=body_params, auth=(
            os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET']))

        token_raw = json.loads(response.text)
        token = token_raw["access_token"]
        token_object = {"TOKEN": token}
        status = write_json(os.path.join('config', 'token.json'), token_object)
        if not status:
            print("unable to update token")
        return token
    except:
        return None


def read_json(file_path):
    """Reads a json file for given path

    Args:
        file_path (string): filepath of json file to read

    Returns:
        dict: contents of given file
    """
    with open(file_path) as f:
        data = json.load(f)
    return data


def write_json(filepath, dictionary):
    """Writes a json file for given path for given content

    Args:
        filepath (string): filepath to write path as
        dictionary (dict): contents to write in a file

    Returns:
        bool: status if the action is successful or not
    """
    try:
        with open(filepath, 'w') as json_file:
            json.dump(dictionary, json_file)
            print("CHANGED")
        return True
    except:
        return False


def get_header(token):
    """For a given token return a request header

    Args:
        token (string): spotify auth token

    Returns:
        dict: A request header
    """
    return {
        'Authorization': 'Bearer {token}'.format(token=token)
    }


def search_track(query, market):
    """Returns the details of a track for the given search query.

    Args:
        query (string): Search query
        market (string): Country in available_market

    Returns:
        list: List of dictionaries. Each dictionary contains details of a track.
    """
    try:
        print("IN", query, market)
        url = f"https://api.spotify.com/v1/search?q={query.replace(' ','%20')}&type=track&limit=20&market={market}"
        token = read_json(os.path.join('config', 'token.json'))['TOKEN']
        headers = get_header(token)
        response = requests.get(url, headers=headers)
        if response.status_code is not 200:
            token = renew_auth_token(
                read_json(os.path.join('config', 'credentials.json')))
            headers = get_header(token)
            response = requests.get(url, headers=headers)
        response_data = response.json()
        container = []
        for item in response_data['tracks']['items']:
            container.append(parse_track(item))
        return container
    except:
        return []


def search_playlist(query, market):
    """Returns the details of a playlist for the given search query.

    Args:
        query (string): Search query
        market (string): Country in available_market

    Returns:
        list: List of dictionaries. Each dictionary contains details of a playlist.
    """
    try:
        url = f"https://api.spotify.com/v1/search?q={query}&type=playlist&limit=5&market={market}"
        token = read_json(os.path.join('config', 'token.json'))['TOKEN']
        headers = get_header(token)
        response = requests.get(url, headers=headers)
        if response.status_code is not 200:
            token = renew_auth_token(
                read_json(os.path.join('config', 'credentials.json')))
            headers = get_header(token)
            response = requests.get(url, headers=headers)
        response_data = response.json()
        container = []

        for item in response_data['playlists']['items']:
            container.append(parse_playlist(item))
        return container
    except:
        return []


def get_a_playlist(playlist_id):
    """Get tracks of a playlist for the given playlist_id

    Args:
        playlist_id (string): SpotifyId of a playlist

    Returns:
        list: List of dictionaries. Each dictionary contains details of the track in the playlist.
    """
    try:
        url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        token = read_json(os.path.join('config', 'token.json'))['TOKEN']
        headers = get_header(token)
        response = requests.get(url, headers=headers)
        if response.status_code is not 200:
            token = renew_auth_token(
                read_json(os.path.join('config', 'credentials.json')))
            headers = get_header(token)
            response = requests.get(url, headers=headers)
        response_data = response.json()
        container = []
        # print("response_data",response_data)
        for item in response_data['tracks']['items']:
            container.append(parse_track(item['track']))
        return container
    except:
        return []


def parse_playlist(playlist):
    """Selects only needed attributes from details of a playlist

    Args:
        playlist (dict): contents of a playlist

    Returns:
        dict: filtered details from given data
    """
    try:
        filtered_data = {key: playlist[key] for key in ['id', 'name']}
        filtered_data.update(
            {'owner': playlist['owner']['display_name'],
             'href': playlist['external_urls']['spotify']})
        return filtered_data
    except:
        return {}


def parse_track(track):
    """Selects only needed attributes from details of a track

    Args:
        track (dict): contents of a track

    Returns:
        dict: filtered details from given data
    """
    try:
        filtered_data = {key: track[key]
                         for key in ['id', 'name', 'preview_url']}
        artists = ','.join([section['name']
                            for section in track['album']['artists']])
        filtered_data.update(
            {'album': track['album']['name'], 'artist': artists})
        return filtered_data
    except:
        return {}


def get_available_countries():
    countries = read_json(os.path.join('static', 'countries.json'))
    return countries


def send_cache_clear_request(country):
    """Send request to clear cache with api-key

    Returns:
        dict: response with status message
    """
    print("main_to_clear")
    attributes = read_json(os.path.join(
        'config', 'cacheClearRequestItems.json'))
    mutation = '''
            mutation InvalidateCache {
        InvalidateCache(key: "tt-service-catalog-production-get-all-playlists-%s-response") {
            __typename
            ...on InvalidateCacheSuccess {
            __typename
            message
            }
            ...on InvalidParameterErrors {
            __typename
            errors {
                field
                message
            }
            }
            ...on InternalServerError {
            __typename
            message
            }
        }
        }

    ''' % country
    status = requests.post(attributes['url'], json={
                           'query': mutation}, headers=attributes['headers'])
    if 'data' in status.json():
        return {"message": status.json()['data']['InvalidateCache']['message']}
    else:
        return {"message": "Oops! Please try again"}

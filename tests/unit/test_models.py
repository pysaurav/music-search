""" Tests for models where the application interacts with SpotifyAPI
"""
import pytest
import requests_mock
from Models.models import search_track, search_playlist

#pylint: disable= E0401
#pylint: disable= W0621
# Disabling import error as the import has no issues with pytest
# Disabling scope error since pytest fixture runs using it


@pytest.fixture()
def track_search_response():
    """Returns sample response for search_track get request

    Returns:
        dictionary: sample track response from spotify
    """
    response = {'tracks':
                {'herf': 'SAMPLE_URL',
                 'items': [
                     {'preview_url': 'SAMPLE_PREVIEW_URL_1',
                      'name': 'SAMPLE_TITLE_1',
                      'id': 'SAMPLE_ID_1',
                      'album': {'name': 'SAMPLE_ALBUM_NAME_1',
                                'artists': [{'name': 'SAMPLE_ARTIST_1'}]
                                }},
                     {'preview_url': 'SAMPLE_PREVIEW_URL_2',
                      'name': 'SAMPLE_TITLE_2',
                      'id': 'SAMPLE_ID_2',
                      'album': {'name': 'SAMPLE_ALBUM_NAME_2',
                                'artists': [{'name': 'SAMPLE_ARTIST_2'}]
                                }}
                 ],
                 'limit': 'SAMPLE_LIMIT'}}
    return response


@pytest.fixture()
def playlist_search_response():
    """Returns sample response for search_playlist get request

    Returns:
        dictionary: sample playlist response from spotify
    """
    response = {'playlists':
                {'href': 'SAMPLE_HREF',
                 'items': [{'collaborative': False,
                            'description': '',
                            'external_urls':
                            {'spotify': 'SAMPLE_URL_TO_PLAYLIST'},
                            'href': 'HREF',
                            'id': 'SAMPLE_ID',
                            'images': [{'height': 640,
                                        'url': 'SAMPLE_IMAGE_URL_640', 'width': 640},
                                       {'height': 300, 'url': 'SAMPLE_IMAGE_URL_300',
                                        'width': 300},
                                       {'height': 60, 'url':
                                           'SAMPLE_IMAGE_URL_60', 'width': 60}],
                            'name': 'SAMPLE_PLAYLIST_NAME',
                            'owner': {'display_name': 'SAMPLE_OWNER_NAME',
                                      'external_urls':
                                      {'spotify': 'SAMPLE_HREF'},
                                      'href': 'SAMPLE_HREF',
                                      'id': 'SAMPLE_OWNER_ID',
                                      'type': 'user',
                                      'uri': 'spotify:user:SAMPLE_OWNER_ID'},
                            'primary_color': None, 'public': None,
                            'snapshot_id': 'SAMPLE_SNAPSHOT_ID',
                            'tracks': {'href': 'SAMPLE_URL_FOR_TRACKS',
                                       'total': 16},
                            'type': 'playlist',
                            'uri': 'spotify:playlist:SAMPLE_ID'}],
                 'limit': 5, 'next': None,
                 'offset': 0, 'previous': None, 'total': 1}}
    return response


def test_search_track(track_search_response):
    """Mocks the get requst for search track and tests our model

    Args:
        track_search_response (dict): sample response for track search from spotify
    """
    with requests_mock.mock() as mocked:
        mocked.get(
            requests_mock.ANY,
            status_code=200,
            json=track_search_response)
        response = search_track("SAMPLE_QUERY")
        assert response == [{'id': 'SAMPLE_ID_1', 'name': 'SAMPLE_TITLE_1',
                             'preview_url': 'SAMPLE_PREVIEW_URL_1', 'album':
                                 'SAMPLE_ALBUM_NAME_1', 'artist': 'SAMPLE_ARTIST_1'},
                            {'id': 'SAMPLE_ID_2', 'name': 'SAMPLE_TITLE_2',
                             'preview_url': 'SAMPLE_PREVIEW_URL_2', 'album':
                                 'SAMPLE_ALBUM_NAME_2', 'artist': 'SAMPLE_ARTIST_2'}]


def test_search_playlist(playlist_search_response):
    """Mocks the get requst for search playlist and tests our model

    Args:
        playlist_search_response (dict): sample response for playlist search from spotify
    """
    with requests_mock.mock() as mocked:
        mocked.get(
            requests_mock.ANY,
            status_code=200,
            json=playlist_search_response)
        response = search_playlist("SAMPLE_QUERY")
        assert response == [{'id': 'SAMPLE_ID',
                             'name': 'SAMPLE_PLAYLIST_NAME',
                             'owner': 'SAMPLE_OWNER_NAME',
                             'href': 'SAMPLE_URL_TO_PLAYLIST'
                             }]

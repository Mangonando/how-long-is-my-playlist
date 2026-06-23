import spotipy
from django.conf import settings
from spotipy.oauth2 import SpotifyOAuth


def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope=settings.SPOTIFY_SCOPE,
        cache_path=None,
        show_dialog=True,
    )


def get_auth_url():
    spotify_oauth = get_spotify_oauth()
    return spotify_oauth.get_authorize_url()


def get_token_from_code(code):
    spotify_oauth = get_spotify_oauth()
    return spotify_oauth.get_access_token(code, check_cache=False)


def get_spotify_client(token_info):
    return spotipy.Spotify(auth=token_info["access_token"])

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


def get_valid_token_info(request):
    token_info = request.session.get("spotify_token_info")

    if not token_info:
        return None

    spotify_oauth = get_spotify_oauth()

    if spotify_oauth.is_token_expired(token_info):
        token_info = spotify_oauth.refresh_access_token(token_info["refresh_token"])
        request.session["spotify_token_info"] = token_info

    return token_info


def get_spotify_client(token_info):
    return spotipy.Spotify(auth=token_info["access_token"])


def get_user_playlists(spotify):
    playlists = []
    response = spotify.current_user_playlists(limit=50)

    while response:
        playlists.extend(response["items"])

        if response["next"]:
            response = spotify.next(response)
        else:
            response = None

    return playlists


def get_playlist_details(spotify, playlist_id):
    return spotify.playlist(
        playlist_id,
        fields="id,name,images,owner(display_name),tracks(total)",
    )


def get_playlist_tracks(spotify, playlist_id):
    tracks = []

    response = spotify.playlist_items(
        playlist_id,
        limit=100,
    )

    while response:
        for item in response["items"]:
            if not item:
                continue
            track = item.get("item")

            if not track:
                continue

            duration_ms = track.get("duration_ms")

            if duration_ms is None:
                continue

            tracks.append(
                {
                    "id": track.get("id"),
                    "name": track.get("name", "Unknown track"),
                    "duration_ms": duration_ms,
                    "artists": [artist["name"] for artist in track.get("artists", [])],
                }
            )

        if response["next"]:
            response = spotify.next(response)
        else:
            response = None

    return tracks

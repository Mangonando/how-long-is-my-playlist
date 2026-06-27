from django.shortcuts import redirect, render
from spotipy.exceptions import SpotifyException

from project import (
    calculate_adjusted_duration,
    calculate_crossfade_loss,
    format_duration,
)

from .spotify import (
    get_auth_url,
    get_playlist_details,
    get_playlist_tracks,
    get_spotify_client,
    get_token_from_code,
    get_user_playlists,
    get_valid_token_info,
)


def spotify_login(request):
    return redirect(get_auth_url())


def spotify_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect("calculator")
    spotify_token_info = get_token_from_code(code)
    request.session["spotify_token_info"] = spotify_token_info
    return redirect("playlists")


def spotify_logout(request):
    request.session.flush()
    return redirect("calculator")


def calculator(request):
    if request.method == "POST":
        return redirect("calculator")

    spotify_logged_in = "spotify_token_info" in request.session
    return render(
        request,
        "playlists/calculator.html",
        {
            "spotify_logged_in": spotify_logged_in,
            "show_playlists_nav": spotify_logged_in,
        },
    )


def playlists_view(request):
    spotify_token_info = get_valid_token_info(request)

    if not spotify_token_info:
        return redirect("spotify_login")

    spotify = get_spotify_client(spotify_token_info)
    playlists = get_user_playlists(spotify)

    search_query = request.GET.get("q", "").strip().lower()

    if search_query:
        playlists = [
            playlist
            for playlist in playlists
            if search_query in playlist["name"].lower()
        ]
    return render(
        request,
        "playlists/playlists.html",
        {
            "playlists": playlists,
            "search_query": search_query,
            "spotify_logged_in": True,
        },
    )


def playlist_detail_view(request, playlist_id):
    spotify_token_info = get_valid_token_info(request)

    if not spotify_token_info:
        return redirect("spotify_login")

    spotify = get_spotify_client(spotify_token_info)

    try:
        playlist = get_playlist_details(spotify, playlist_id)
        tracks = get_playlist_tracks(spotify, playlist_id)
    except SpotifyException:
        return render(
            request,
            "playlists/playlist_detail.html",
            {
                "access_error": True,
                "spotify_logged_in": True,
            },
        )

    total_milliseconds = sum(track["duration_ms"] for track in tracks)
    total_seconds = total_milliseconds // 1000
    song_count = len(tracks)

    crossfade_error = None

    try:
        crossfade_seconds = int(request.GET.get("crossfade", 12))
        if not 0 <= crossfade_seconds <= 12:
            raise ValueError
    except ValueError:
        crossfade_seconds = 12
        crossfade_error = "Crossfade must be between 0 and 12"

    if song_count == 0:
        reduction_seconds = 0
        adjusted_seconds = 0
    else:
        reduction_seconds = calculate_crossfade_loss(song_count, crossfade_seconds)
        adjusted_seconds = calculate_adjusted_duration(
            total_seconds,
            song_count,
            crossfade_seconds,
        )

    return render(
        request,
        "playlists/playlist_detail.html",
        {
            "playlist": playlist,
            "tracks": tracks,
            "song_count": song_count,
            "crossfade_seconds": crossfade_seconds,
            "crossfade_error": crossfade_error,
            "original_duration": format_duration(total_seconds),
            "reduction_duration": format_duration(reduction_seconds),
            "adjusted_duration": format_duration(adjusted_seconds),
            "spotify_logged_in": True,
        },
    )

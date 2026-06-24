from django.shortcuts import redirect, render

from .spotify import (
    get_auth_url,
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

    spotify_connected = "spotify_token_info" in request.session
    return render(
        request, "playlists/calculator.html", {"spotify_connected": spotify_connected}
    )


def playlists_view(request):
    spotify_token_info = get_valid_token_info(request)

    if not spotify_token_info:
        return redirect("spotify_login")

    playlists = get_user_playlists(spotify_token_info)

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
            "spotify_connected": True,
        },
    )

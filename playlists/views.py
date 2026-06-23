from django.shortcuts import redirect, render

from .spotify import get_auth_url, get_token_from_code


def spotify_login(request):
    return redirect(get_auth_url())


def spotify_callback(request):
    code = request.GET.get("code")
    if not code:
        return redirect("calculator")
    token_info = get_token_from_code(code)
    request.session["token_info"] = token_info
    return redirect("calculator")


def spotify_logout(request):
    request.session.flush()
    return redirect("calculator")


def calculator(request):
    if request.method == "POST":
        return redirect("calculator")

    spotify_connected = "token_info" in request.session
    return render(
        request, "playlists/calculator.html", {"spotify_connected": spotify_connected}
    )

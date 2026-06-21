from django.shortcuts import redirect, render


def calculator(request):
    if request.method == "POST":
        return redirect("calculator")

    return render(request, "playlists/calculator.html")

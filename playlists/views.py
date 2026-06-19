from django.shortcuts import render

from project import (
    calculate_total_seconds,
    calculate_adjusted_duration,
    format_duration,
)


def calculator(request):
    result = None

    form_data = {
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
        "song_count": 1,
        "crossfade_seconds": 0,
    }

    if request.method == "POST":
        form_data = {
            "hours": int(request.POST.get("hours", 0)),
            "minutes": int(request.POST.get("minutes", 0)),
            "seconds": int(request.POST.get("seconds", 0)),
            "song_count": int(request.POST.get("song_count", 1)),
            "crossfade_seconds": int(request.POST.get("crossfade_seconds", 0)),
        }

        total_seconds = calculate_total_seconds(
            form_data["hours"],
            form_data["minutes"],
            form_data["seconds"],
        )

        adjusted_seconds = calculate_adjusted_duration(
            total_seconds,
            form_data["song_count"],
            form_data["crossfade_seconds"],
        )

        result = format_duration(adjusted_seconds)

    return render(request, "playlists/calculator.html", {
        "result": result,
        "form_data": form_data,
    })

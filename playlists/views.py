from django.shortcuts import render

from project import (
    calculate_total_seconds,
    calculate_adjusted_duration,
    format_duration,
)

def calculator(request):
    result = None
    
    if request.method == "POST":
        hours = int(request.POST.get("hours", 0))
        minutes = int(request.POST.get("minutes", 0))
        seconds = int(request.POST.get("seconds", 0))
        song_count = int(request.POST.get("song_count", 0))
        crossfade_seconds = int(request.POST.get("crossfade_seconds", 0))

        total_seconds = calculate_total_seconds(hours, minutes, seconds)
        adjusted_seconds = calculate_adjusted_duration(total_seconds, song_count, crossfade_seconds)

        result = format_duration(adjusted_seconds)

    return render(request, "playlists/calculator.html", {
        "result": result
    })
def main():
    hours = int(input("Hours: "))
    minutes = int(input("Minutes: "))
    seconds = int(input("Seconds: "))
    song_count = int(input("Number of songs: "))
    crossfade_seconds = int(input("Crossfade in seconds: "))

    total_seconds = calculate_total_seconds(hours, minutes, seconds)
    adjusted_seconds = calculate_adjusted_duration(
        total_seconds, song_count, crossfade_seconds
    )

    print(format_duration(adjusted_seconds))


def calculate_total_seconds(hours, minutes, seconds):
    return hours * 3600 + minutes * 60 + seconds


def calculate_crossfade_loss(song_count, crossfade_seconds):
    if song_count <= 1:
        return 0

    return (song_count - 1) * crossfade_seconds


def calculate_adjusted_duration(total_seconds, song_count, crossfade_seconds):
    total_crossfade_loss = calculate_crossfade_loss(song_count, crossfade_seconds)
    adjusted_seconds = total_seconds - total_crossfade_loss

    if adjusted_seconds < 0:
        return 0

    return adjusted_seconds


def format_duration(total_seconds):
    hours = total_seconds // 3600
    remaining_seconds = total_seconds % 3600

    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"

    return f"{minutes}:{seconds:02}"


if __name__ == "__main__":
    main()

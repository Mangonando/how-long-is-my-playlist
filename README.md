# How Long Is My Playlist?

#### Video Demo: <URL HERE>

#### Description:

**How Long Is My Playlist?** (HLIMP) is a web application that calculates the real duration of a music playlist after crossfade is applied.
The project started as a command-line Python script and evolved into a full Django web application with a clean, responsive UI.

---

## Why this project?

When you enable crossfade in a music player like Spotify, each song fades into the next which means the actual listening time is shorter than the sum of all song durations. This tool lets you enter your playlist's total duration, the number of songs, and your crossfade setting to get the adjusted, real-world duration.
I couldn't find a simple tool to calculate this, so I built one.

---

## Tech Stack

- **Python 3.9**
- **Django 4.2**
- **HTML / CSS / JavaScript**
- **python-dotenv** for environment variable management

---

## Project Structure

```
how-long-is-my-playlist/
├── project.py                          # CLI version (core logic)
├── hlimp_site/                         # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── playlists/                          # Django app
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── playlists/
│           ├── base.html              # Base layout template
│           └── calculator.html        # Calculator page
├── requirements.txt
└── pyproject.toml                      # Ruff linter/formatter config
```

---

## Files explained

### `project.py`

This is the original command-line version of the calculator and contains the core business logic of the project. It defines four functions:

- `calculate_total_seconds(hours, minutes, seconds)` — converts the playlist duration to a single integer in seconds.
- `calculate_crossfade_loss(song_count, crossfade_seconds)` — calculates how many seconds are lost to crossfade. The formula is `(song_count - 1) * crossfade_seconds`, since the last song has no fade-out into a next track.
- `calculate_adjusted_duration(total_seconds, song_count, crossfade_seconds)` — subtracts the crossfade loss from the total, clamping at zero to avoid negative durations.
- `format_duration(total_seconds)` — formats the result as `H:MM:SS` or `M:SS` depending on whether the duration exceeds an hour.

The `main()` function collects user input via the terminal and prints the result. This script can be run independently without Django.

### `playlists/views.py`

The Django view for the calculator. It handles both GET and POST requests to the `/` route. On GET, it renders the calculator template. On POST, it redirects back to the same page, a standard POST/Redirect/GET pattern that prevents form resubmission on browser refresh. The actual calculation is done entirely client-side in JavaScript, so no data processing happens in the view for this version of the app.

### `playlists/templates/playlists/base.html`

The base HTML template that all pages inherit from using Django's template inheritance system (`{% extends %}`). It defines the overall page structure: the `<head>` with CSS links and favicon, the navigation bar with the HLIMP logo and links, a mobile hamburger menu with overlay. The mobile menu is handled with a small inline JavaScript snippet that toggles CSS classes.

### `playlists/templates/playlists/calculator.html`

The main page of the application. It extends `base.html` and contains two sections:

1. **Heading section** — a heading and short description of what the tool does.
2. **Calculator card** — a form with inputs for hours, minutes, seconds, number of songs, and a range slider for the crossfade duration (1–12 seconds). The form submits via POST but the result is computed and displayed entirely in JavaScript without a page reload.

The JavaScript in this template mirrors the logic from `project.py` exactly:
- Input validation restricts number fields to digits only and enforces per-field limits (e.g., minutes and seconds cap at 59).
- The crossfade slider updates a live display label as it moves.
- On form submit, `calculateAdjustedDuration()` runs the same formula as the Python backend and injects a result card below the form.

### `pyproject.toml`

Configuration for [Ruff](https://docs.astral.sh/ruff/), the Python linter and formatter used in this project. It targets Python 3.9, enforces an 88-character line length, and enables rules for pycodestyle, pyflakes, isort, and Django-specific checks. A pre-commit hook runs Ruff automatically before every `git commit`.

---

## Design choices

**Why compute client-side instead of server-side?**
The calculation is stateless and simple — no database, no user accounts, no sensitive data. Doing it in JavaScript means instant feedback without a round trip to the server. The trade-off is that logic lives in two places (Python and JS), but the functions are short enough that keeping them in sync is not a real burden.

**Why Django for something this simple?**
The goal was to learn Django, not to pick the most minimal tool. Using Django for a small project is a deliberate learning choice — it exposes you to the full request/response cycle, URL routing, template inheritance, static files, and settings management in a controlled environment.

**Why a range slider for crossfade?**
Crossfade in Spotify goes from 1 to 12 seconds. A slider communicates that this is a bounded, continuous value and feels more natural than typing a number. It also allows for real-time result updates when a result is already displayed.

---

## How to run

### Requirements

- Python 3.9+
- pip

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd how-long-is-my-playlist

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file with a secret key
echo "SECRET_KEY=your-secret-key-here" > .env

# Run the development server
python manage.py runserver
```

Then open http://127.0.0.1:8000 in your browser.

### Run the CLI version

```bash
python project.py
```

---

## Optional: Linting

```bash
pip install ruff
ruff check .
ruff format .
```

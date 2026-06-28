# How Long Is My Playlist?

#### Video Demo: <URL HERE>

#### Description:

**How Long Is My Playlist?** (HLIMP) calculates the real duration of a Spotify playlist after crossfade is applied. The project started as a command-line Python script and evolved into a full Django web application with Spotify OAuth integration and a clean, responsive UI.

---

## Why this project?

When crossfade is enabled in Spotify, each song fades into the next — so the actual listening time is shorter than the sum of all song durations. I couldn't find a simple tool to calculate this, so I built one.

---

## Tech Stack

- Python 3.9 · Django 4.2 · Spotipy 2.26
- HTML / CSS / JavaScript
- python-dotenv

---

## Project Structure

```
how-long-is-my-playlist/
├── project.py              # Core logic + CLI entry point
├── hlimp_site/             # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── playlists/              # Django app
│   ├── views.py
│   ├── urls.py
│   ├── spotify.py          # Spotify OAuth and API helpers
│   └── templates/playlists/
│       ├── base.html       # Base layout
│       ├── calculator.html # Manual calculator page
│       ├── playlists.html  # Spotify playlists grid
│       └── playlist_detail.html
├── requirements.txt
└── pyproject.toml          # Ruff config
```

---

## Files explained

**`project.py`** — Core business logic shared by the CLI and the web app: `calculate_total_seconds`, `calculate_crossfade_loss` (`(song_count - 1) * crossfade_seconds`), `calculate_adjusted_duration`, and `format_duration`. The `main()` function runs a terminal prompt independently of Django.

**`playlists/spotify.py`** — All Spotify logic in one place: OAuth 2.0 Authorization Code Flow (auth URL, token exchange, token refresh), an authenticated Spotipy client, and paginated API calls to fetch playlists, metadata, and tracks.

**`playlists/views.py`** — All Django views: `calculator`, `spotify_login`, `spotify_callback`, `spotify_logout`, `playlists_view`, and `playlist_detail_view`. The detail view catches `SpotifyException` (e.g. 403 on restricted playlists) and renders a friendly error instead of crashing.

**`base.html`** — Shared layout with a navbar whose links adapt based on login state and current page, plus a responsive mobile menu with hamburger button and overlay.

**`calculator.html`** — Manual calculator with time inputs, song count, and a crossfade slider (0–12 s). Calculation runs in JavaScript, mirroring the `project.py` logic.

**`playlists.html`** — Responsive grid of the user's Spotify playlists with cover art, name, and track count. Includes server-side search filtering by name.

**`playlist_detail.html`** — Playlist cover, metadata, crossfade slider (recalculates on submit), original vs. real duration, and a full numbered track list. Shows a friendly error if the playlist is inaccessible.

**`pyproject.toml`** — [Ruff](https://docs.astral.sh/ruff/) config: Python 3.9, 88-char line length, pycodestyle/pyflakes/isort/Django rules. Pre-commit hook runs on every `git commit`.

---

## Design choices

**Client-side calculation (manual calculator)** — The math is stateless with no sensitive data involved, so JavaScript gives instant feedback without a server round trip. The logic mirrors `project.py` exactly.

**Crossfade as a slider** — A 0–12 s bounded range is more intuitive as a slider than a text input. On the detail page, submitting the form recalculates on the server with the new value.

**Spotify integration alongside manual input** — The manual calculator requires knowing total duration, song count, and crossfade upfront. Spotify integration fetches all of that automatically. Both modes coexist for users without a Spotify account.

---

## How to run

Requires Python 3.9+ and a Spotify app ([create one here](https://developer.spotify.com/dashboard)).

```bash
git clone <repo-url>
cd how-long-is-my-playlist

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
SPOTIFY_CLIENT_ID=your-client-id
SPOTIFY_CLIENT_SECRET=your-client-secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8000/callback/
```

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

**CLI only:** `python project.py`

**Linting:** `ruff check . && ruff format .`

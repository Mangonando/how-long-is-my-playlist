# How Long Is My Playlist?

#### Video Demo: https://www.youtube.com/watch?v=BSKYFKdOkmY

#### Description:

**How Long Is My Playlist?** (HLIMP) calculates the real duration of a Spotify playlist after crossfade is applied. The project started as a command-line Python script and evolved into a full Django web application with Spotify OAuth integration and a clean, responsive UI.


#### Webapp Sample:

![Screenshot](screenshots/Screenshot%202026-06-30%20at%2014.18.44.png)
![Screenshot](screenshots/Screenshot%202026-06-30%20at%2014.22.58.png)
![Screenshot](screenshots/Screenshot%202026-06-30%20at%2014.25.47.png)
![Screenshot](screenshots/Screenshot%202026-06-30%20at%2014.26.28.png)
![Screenshot](screenshots/Screenshot%202026-06-30%20at%2014.27.02.png)
![Screenshot](screenshots/Screenshot%202026-06-30%20at%2014.27.52.png)

## Why this project?

When crossfade is enabled in Spotify, each song fades into the next, the actual listening time is shorter than the sum of all song durations. I couldn't find a simple tool to calculate this, so I built one.


## Tech Stack

- Python 3.9 · Django 4.2 · Spotipy 2.26
- HTML / CSS / JavaScript
- python-dotenv


## Project Structure

```
how-long-is-my-playlist/
├── project.py              # Core logic + CLI entry point
├── test_project.py         # pytest tests for core functions
├── manage.py               # Django management CLI
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


## Design choices

**Client-side calculation (manual calculator)**: The math is stateless with no sensitive data involved, I had to use JavaScript to get an instant feedback without a server round trip. The logic mirrors `project.py`.

**Crossfade as a slider**: Most of the information is added in an input. However, to improve the user experience I added a slider. it will be more intuitive and it will look better too. It is also self informative so users know what to do with it. 

**Manual Calculator**: I want to have a placeholdere where every user independently of where they have their playlist could check its length manually.

**Spotify integration alongside manual input**: The most popular platform to date is Spotify. I want it to integrate it and fetch all the playlists automatically. This way it provides a better user experience without neglecting users who don`t have spotify. 

**Spotify Login**: I chose it in order to fetch the playlists. Using other ways of login such as google, or apple would have been overengineering and useless as the user would not have got a better experience if they login that way.

**Spotify Oauth**: I used Oauth to allow HLIMP to fetch the data automatically. It was better than parsing the playlist url.


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


## Deploying (Railway or Render)

1. Push the repo to GitHub
2. Create a new project on [Railway](https://railway.app) or [Render](https://render.com) and connect the repo
3. Set the following environment variables in the platform dashboard:

```
SECRET_KEY=a-long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=your-app-domain.railway.app
SPOTIFY_CLIENT_ID=your-client-id
SPOTIFY_CLIENT_SECRET=your-client-secret
SPOTIFY_REDIRECT_URI=https://your-app-domain.railway.app/callback/
```

4. Add `https://your-app-domain.railway.app/callback/` as a Redirect URI in your [Spotify app settings](https://developer.spotify.com/dashboard)
5. The `Procfile` handles migrations, static file collection, and starting the server automatically


## AI assistance
This project was built with the assistance of Claude (Anthropic) as an AI pair programmer. Claude was used to discuss architectural approaches, explore design tradeoffs, review naming and code clarity, and speed up implementation. All design decisions, feature choices, and direction were made by the author. The AI served as an amplifier, not as a replacement for understanding.

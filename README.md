### INF601 - Advanced Programming in Python
### Jeff Johnson
### Mini Project 3
 
 
## Mini Project 3 — Bama Pick ’Em (Flask Web App)
 
A small Flask web app where users predict Alabama football scores, earn points, and climb a leaderboard.

## Description
 
What this app does

- Pages (6): Home, Schedule, Make/Edit Pick, My Picks, Leaderboard, About/Rules
- Auth: Register, login, logout (session-based)
- Picks: One pick per user per game, editable until the game is Final
- Scoring: 0–50 points per game
- Raw = winner_bonus (10 or 0) - margin_diff - total_diff
- Points = max(0, 40 + Raw) → exact score = 50
- UI: Bootstrap 5 with a required modal (“How to Play”), custom crimson theme
- Data: SQLite with user, game, pick (FKs + unique username)

```
├─ app/
│  ├─ __init__.py           # Flask factory + CLI seed commands
│  ├─ auth.py               # Register/Login/Logout, session auth
│  ├─ db.py                 # SQLite connection + init-db command
│  ├─ main.py               # Pages: home, schedule, pick form, my picks, leaderboard, about
│  ├─ schema.sql            # Tables: user, game, pick (+ indexes)
│  ├─ static/
│  │  ├─ style.css          # Crimson theme + navbar/button tweaks
│  │  └─ logo.svg           # Alabama "script A" (local asset)
│  └─ templates/
│     ├─ base.html          # Bootstrap layout + How-to-Play modal
│     ├─ index.html         # Home
│     ├─ about.html         # About & detailed rules
│     ├─ schedule.html      # Game list/cards (shows “Pick made” if applicable)
│     ├─ pick_form.html     # Make/Edit Pick (GET/POST)
│     ├─ mypicks.html       # User’s picks
│     ├─ leaderboard.html   # Ranked scores
│     ├─ auth/
│     │  ├─ login.html
│     │  ├─ register.html
│     │  └─ login_redirect.html  # 5s pause after login → Home
│     └─ partials/
│        └─ rules_core.html  # Shared rules used by modal + About
├─ instance/
│  └─ app.db               # (created at runtime)
├─ requirements.txt
└─ README.md  (this file)
```

Database Schema:
- user: id, username (UNIQUE COLLATE NOCASE), password, created_at
- game: id, week, date, opponent, location, bama_is_home, final_bama, final_opp
- pick: id, user_id → user.id, game_id → game.id, pred_bama, pred_opp, created_at, UNIQUE(user_id, game_id)

Foreign keys are enforced (PRAGMA foreign_keys = ON). See app/schema.sql.

## Using The App

1. Create your account
   - Go to Register and choose a username and password. Usernames are unique (case-insensitive).

2. Log in
   - Sign in on Login. You’ll see a brief “Login successful” screen (about 5 seconds), then you’ll land on Home.

3. Make a pick
   - Open Schedule → choose an upcoming game → click Make / Edit Pick.
   - Enter your predicted scores for Alabama and the opponent, then Save.
   - You can change your pick any time until the game is marked Final.

4. Check your picks
   - Go to My Picks to see everything you’ve submitted.
   - For games that aren’t Final yet, you can click Edit Pick to update your scores.

5. See the standings
   - Visit Leaderboard to view rankings once results exist.
   - Scoring is 0–50 points per game (exact score = 50). Higher total = higher rank.

Quick rules
Click How to Play in the navbar for a quick summary.
For detailed scoring examples, open About.

Tip: On the Schedule page, you’ll see a small green “Pick made” tag on games you’ve already picked.
 
### Dependencies
 
- Python 3.13.7
- Operating System: 
    - Windows

- Required libraries (install with pip):
```
pip install -r requirements.txt
```

## Installing
 
1. Clone or download this project to your local machine.
2. Go to the project root.
3. Ensure you have the required dependencies listed above installed
   - pip install -r requirements.txt
4. Initialize a fresh database
   - flask --app app:create_app init-db
5. Seed the 2025 schedule and apply finals for played games
   - flask --app app:create_app seed-games-2025
   - flask --app app:create_app seed-finals-2025
6. Create demo users (all passwords = 'password')
   - flask --app app:create_app seed-users -n 12
7. Create random picks for completed games
   - flask --app app:create_app seed-random-picks
8. Verify data
   - flask --app app:create_app show-games
 
## Executing program

Run the server
```
flask --app app:create_app run --debug
```
The server will run on http://127.0.0.1:5000
 
## Help
 
If you encounter issues, re-run pip installs and re-seed the app settings:
```
pip install -r requirements.txt
flask --app app:create_app init-db
flask --app app:create_app seed-games-2025
flask --app app:create_app seed-finals-2025
flask --app app:create_app seed-users -n 12
flask --app app:create_app seed-random-picks
flask --app app:create_app show-games
flask --app app:create_app run --debug
```
 
## Authors
 
Jeff Johnson
 
## Version History
 
- 0.1
  - Initial Release
 
## License
 
This project is licensed under the MIT License - see the LICENSE.md file for details
 
## Acknowledgments
 
Inspiration, code snippets, etc.
- [Flask Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/)
- [ChatGPT](https://chatgpt.com/g/g-p-68e844d65ae48191943f2b20b65971dc-mini-project-three/project)
*** I use a ChatGPT paid acct, so I cannot share ***


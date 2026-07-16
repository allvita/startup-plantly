# PlantCare AI — Phase 1

A calm, premium, living home for your plants — not an IoT dashboard, not an admin panel.
Built with FastAPI, Jinja2, TailwindCSS, HTMX, Alpine.js, Chart.js and SQLite.

## ✨ What's inside

- **Beautiful authentication** — dark, animated login screen with a floating gradient
  background, password visibility toggle, remember-me, and hashed-password sessions.
- **Living dashboard** — animated circular health score, four live sensor cards,
  a premium care timeline, a "Next Recommended Action" card, human-language
  garden insights, and smooth Chart.js trend charts.
- **Two demo plants** — Tomato (soft tomato-red accent) and Potato (earthy brown
  accent) — selecting one smoothly swaps the whole dashboard via HTMX, no page reload.
- **Full page set** — Dashboard, My Plants, Plant Details, Calendar, Analytics,
  Settings and Profile.
- **Dark & light mode** — remembered across visits, with a soft green OLED-friendly
  dark theme and a fresh, minimal light theme.
- **Fully responsive** — desktop-first, adapts cleanly down to tablet and mobile.

## 🧱 Tech stack

| Layer        | Choice                          |
|--------------|----------------------------------|
| Backend      | FastAPI + Uvicorn                |
| Templates    | Jinja2                           |
| Styling      | TailwindCSS (CDN, custom config) |
| Interactivity| HTMX + Alpine.js                 |
| Charts       | Chart.js                         |
| Icons        | Lucide                           |
| Database     | SQLite + SQLAlchemy              |
| Auth         | Server-side sessions (PBKDF2-hashed passwords) |

## 🚀 Running locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then open **http://127.0.0.1:8000**.

The SQLite database (`plantcare.db`) and demo data (one user, two plants,
six care tasks each, and seven days of sensor history) are created and
seeded automatically on first run — nothing else to configure.

### Demo account

| Email               | Password  |
|----------------------|-----------|
| admin@plantcare.ai   | admin123  |

## 📁 Project structure

```
plantcare/
├── app.py                  # FastAPI entrypoint, session middleware, router mounting
├── config.py                # Settings (secret key, DB url, default account)
├── database.py               # SQLAlchemy engine / session / Base
├── models.py                  # User, Plant, CareTask, SensorReading
├── auth.py                     # Password hashing + session helpers
├── crud.py                      # Queries + demo-data seeding
├── insights.py                   # Friendly, human-language garden insights
├── requirements.txt
├── render.yaml                    # Render.com deployment config
├── routes/
│   ├── auth_routes.py               # /login, /logout
│   ├── dashboard_routes.py           # /, /plants/{id}/panel, /api/plants/{id}/chart-data
│   └── plant_routes.py                # /plants, /plants/{id}/details, /calendar, /analytics, /settings, /profile
├── templates/
│   ├── base.html                        # Shell: Tailwind config, fonts, HTMX/Alpine/Chart.js/Lucide
│   ├── login.html
│   ├── dashboard.html
│   ├── my_plants.html
│   ├── plant_details.html
│   ├── calendar.html
│   ├── analytics.html
│   ├── settings.html
│   ├── profile.html
│   └── partials/
│       ├── sidebar.html
│       ├── topbar.html
│       └── dashboard_panel.html        # Swapped via HTMX when a plant is selected
└── static/
    ├── css/style.css            # Glassmorphism, progress rings, motion, accessibility
    ├── js/main.js                 # Count-ups, progress rings, Chart.js, HTMX re-init
    └── images/{tomato,potato}.svg    # Original, hand-built plant illustrations
```

## 🎨 Design system

| Token             | Value      |
|--------------------|------------|
| Primary green       | `#66E15A` |
| Dark background      | `#090909` |
| Dark cards            | `#171717` |
| Light background       | `#F7F8F6` |
| Light cards             | `#FFFFFF` |
| Tomato accent            | `#D95C5C` |
| Potato accent              | `#A67C52` |
| Card radius                  | `28px`   |

Typography pairs **Plus Jakarta Sans** (display/headline) with **Inter** (body/UI).

## 🧠 How plant switching works

Clicking a plant card fires an HTMX `GET /plants/{id}/panel` request that swaps
the `#dashboard-panel` element's contents — sensors, health score, timeline,
insights and charts all update together with a soft fade, and the page never reloads.
A hidden `data-plant-accent` marker on the panel root updates a CSS custom
property (`--accent-secondary`) so borders, highlights and chart lines can lean
on each plant's own accent color without ever overpowering the primary green.

## ☁️ Deploying to Render

This repo ships with a ready-to-use `render.yaml`:

1. Push this project to a GitHub repository.
2. In Render, choose **New → Blueprint** and point it at the repo.
3. Render will install `requirements.txt` and run
   `uvicorn app:app --host 0.0.0.0 --port $PORT` automatically.

## 📌 Phase 1 scope

All sensor data is simulated and seeded on first launch — no physical hardware
or external APIs are required. This lays the foundation for a future phase
where live sensor feeds and AI-generated insights can be plugged directly
into the same `models.py` / `crud.py` structure.

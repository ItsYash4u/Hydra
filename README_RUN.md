Greeva — Run & Setup (Windows cmd.exe)

Summary
- Backend: Django (uses existing `db.sqlite3` at project root).
- Frontend: Vite + React in `client/`.
- All changes are kept inside the `Greeva/` template only.

Prerequisites
- Python 3.12 installed and added to PATH.
- Node.js (>=18) and npm installed.
- Optional: Git if you need to fetch updates.

Backend (create env, install requirements)
Open `cmd.exe` and run:

```
cd \Users\AYUSH\Downloads\admin\Greeva
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements\base.txt
```

Notes:
- The project already includes `db.sqlite3` at the `Greeva/` root. Do NOT delete it unless you intentionally want a fresh DB.
- `manage.py` is configured to use `config.settings.local` by default (development settings).

Run backend dev server:

```
cd \Users\AYUSH\Downloads\admin\Greeva
.venv\Scripts\activate
python manage.py migrate  # safe: will only apply any missing migrations
python manage.py runserver 0.0.0.0:8000
```

Frontend (dev server):
Open a separate terminal and run:

```
cd \Users\AYUSH\Downloads\admin\Greeva\client
npm install
npm run dev
```

- Vite dev server typically runs on `http://localhost:5173/`.
- The Django settings already include CORS allowed origins for `5173` and `3000`.

To serve the production frontend from Django static files (optional):
1. Build the frontend:
```
cd Greeva\client
npm run build
```
2. Copy or configure the built assets into `greeva/static` or serve them from a static host. This template doesn't contain a preconfigured pipeline for auto-copying; do this step manually if you want the frontend to be served by Django.

Database & fixtures
- If fixtures exist under `greeva/fixtures`, you can load them with:
```
python manage.py loaddata <fixture_name>
```
- Otherwise the project will use the included `db.sqlite3`.

Common troubleshooting
- Missing packages: re-run `pip install -r requirements\base.txt`.
- If `pymysql` errors appear, ensure `pymysql` is installed (it may be a dependency of other reqs).

What I changed
- No code changes were required inside the template; configuration already supports the included `db.sqlite3` and frontend dev server.

If you want, I can:
- Add a small `run_dev.cmd` helper to start backend and/or frontend in separate terminals.
- Create a production build flow that copies `client/dist` into `greeva/static` automatically.

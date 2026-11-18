# Flightdeck 747 — Boeing 747-400 website

A responsive Flask website about the Boeing 747-400, with animated UI elements, aircraft facts, copyable research prompts, copyable image-generation/photography prompts, and account registration/sign-in.

## Features

- Responsive dark aviation-inspired interface.
- CSS aircraft illustration, floating animation, reveal-on-scroll cards and mobile navigation.
- Fact cards and a JSON facts endpoint at `/api/facts`.
- Copyable prompts for researching the aircraft and creating aircraft imagery.
- Local account registration, sign-in and sign-out.
- Password hashing using Werkzeug.
- CSRF protection on forms.
- SQLite database via Flask-SQLAlchemy.
- Basic security headers and protected `/explore` page.
- Automated tests using pytest.

The image section contains prompts, not embedded aircraft photographs. Paste a prompt into an image generator or use it as a photography brief. The illustration is an original stylised SVG, not an official Boeing drawing.

## Project structure

```text
boeing_747_400_website/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       └── explore.html
├── tests/
│   ├── conftest.py
│   └── test_site.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

## Requirements

- Python 3.10 or newer.
- pip.
- A modern browser.

## Setup

### 1. Extract and enter the project

```bash
cd boeing_747_400_website
```

### 2. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set a secret key

Create a `.env` file based on `.env.example`, then set `SECRET_KEY` to a long, random value. The app reads environment variables from the process environment; if you use a `.env` file, install and configure `python-dotenv`, or set the variables in your shell.

For a quick local development run, the built-in development key works, but never use it for a public deployment.

Example key generation:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Set it in macOS/Linux:

```bash
export SECRET_KEY="paste-generated-value-here"
```

Windows PowerShell:

```powershell
$env:SECRET_KEY="paste-generated-value-here"
```

### 5. Start the website

```bash
python run.py
```

Open http://127.0.0.1:5000 in your browser. The SQLite database and tables are created automatically when `run.py` starts.

## Run tests

```bash
pytest -q
```

The test suite uses a temporary SQLite database and disables CSRF only in the test configuration. The live application keeps CSRF protection enabled.

## Main routes

| Route | Purpose | Access |
|---|---|---|
| `/` | Home page, facts and prompts | Public |
| `/auth/register` | Create an account | Public |
| `/auth/login` | Sign in | Public |
| `/auth/logout` | Sign out (POST) | Signed-in users |
| `/explore` | Expanded explorer | Signed-in users |
| `/api/facts` | Aircraft facts as JSON | Public |
| `/health` | Basic health check | Public |

## Deploy to Render

The repository includes `render.yaml` for a one-click Blueprint-style deployment. It defines a Python web service, a PostgreSQL database, a generated secret key, HTTPS-only session cookies, and a health check. Render may require a payment method or a paid database plan depending on its current account and region policies.

1. Put this project in a GitHub repository.
2. In Render, choose **New → Blueprint** and select that repository.
3. Review the web service and database resources, then apply the Blueprint.
4. Wait for the build and deployment to finish. Render will show the public `onrender.com` URL.

The database schema is created on startup for this small starter project. For a larger production app, use versioned migrations.

## Production notes

This is a learning/demo website, not an audited production identity platform. Before collecting real user data, add login rate limiting, email verification and password-reset flows, account deletion and retention controls, monitoring, dependency/security scans, and an independent security review. The registration form collects an email address and password, so do not use a personal password or an email address you want to keep private on a demo deployment.

## Accuracy notes

Aircraft details are intentionally presented as introductory facts. Engine options, weights, range, cabin layouts and performance figures vary by aircraft configuration and operator. Verify exact specifications against reliable aviation references before publishing technical claims.

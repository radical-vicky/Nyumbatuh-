# Ultrafy Fiber Network — Django Project

A full-stack Django platform that markets properties for free in exchange for becoming the official fiber internet provider for those buildings.

---

## Tech Stack

| Layer        | Technology                          |
|-------------|--------------------------------------|
| Backend     | Django 5.0                           |
| Auth        | django-allauth + Google OAuth        |
| Database    | PostgreSQL via Neon                  |
| Media       | Cloudinary                           |
| Email       | Gmail SMTP                           |
| Hosting     | Render (or Cloudflare Pages + Workers)|
| Static CDNs | Bootstrap 5, Google Fonts            |
| Styling     | Custom CSS — white & glass-green     |

---

## Local Development Setup

### 1. Clone and enter the project

```bash
git clone <your-repo-url>
cd ultrafy
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install dj-database-url     # needed for DATABASE_URL parsing
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env and fill in all values
```

### 5. Run migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Collect static files

```bash
python manage.py collectstatic
```

### 7. Run the dev server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000`

---

## Environment Variables Reference

| Variable                | Description                                 |
|------------------------|---------------------------------------------|
| `SECRET_KEY`           | Django secret key                           |
| `DEBUG`                | `True` for local, `False` in production     |
| `ALLOWED_HOSTS`        | Comma-separated allowed hosts               |
| `DATABASE_URL`         | PostgreSQL connection string (Neon)         |
| `GOOGLE_CLIENT_ID`     | Google OAuth client ID                      |
| `GOOGLE_CLIENT_SECRET` | Google OAuth client secret                  |
| `CLOUDINARY_CLOUD_NAME`| Your Cloudinary cloud name                  |
| `CLOUDINARY_API_KEY`   | Cloudinary API key                          |
| `CLOUDINARY_API_SECRET`| Cloudinary API secret                       |
| `EMAIL_HOST_USER`      | Gmail address                               |
| `EMAIL_HOST_PASSWORD`  | Gmail App Password (not your Gmail password)|

---

## Setting Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the **Google+ API** and **Google Identity API**
4. Go to **OAuth consent screen** — fill in app name, support email
5. Go to **Credentials → Create OAuth 2.0 Client ID**
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/accounts/google/login/callback/`
   - For production: `https://yourdomain.com/accounts/google/login/callback/`
6. Copy the Client ID and Secret into `.env`
7. In Django admin, go to **Sites** and update the domain
8. Go to **Social Applications → Add** and add Google with your credentials

---

## Setting Up Gmail App Password

1. Enable 2-Factor Authentication on your Google account
2. Go to **Google Account → Security → App Passwords**
3. Generate a new app password for "Mail"
4. Use that 16-character password as `EMAIL_HOST_PASSWORD`

---

## Deploying to Render

1. Push your project to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Render will detect `render.yaml` automatically
5. Set all environment variables in the Render dashboard
6. Deploy

---

## Project Structure

```
ultrafy/
├── ultrafy_core/          # Django settings, main URLs, WSGI
├── accounts/              # User profiles, dashboard, signals
├── properties/            # Property listings, search, inquiries
├── partnerships/          # Partnership applications and status
├── templates/
│   ├── base/              # base.html — navbar, footer, messages
│   ├── account/           # All django-allauth overrides
│   ├── accounts/          # Dashboard, profile edit
│   ├── properties/        # Home, list, detail, create, my properties
│   │   └── partials/      # Reusable property card
│   └── partnerships/      # Landing, apply, status
├── static/
│   ├── css/main.css       # Full white & glass-green theme
│   └── js/main.js         # Nav, image preview, scroll animations
├── manage.py
├── requirements.txt
├── Procfile
├── render.yaml
└── .env.example
```

---

## URL Map

| URL                              | View                   | Auth required |
|---------------------------------|------------------------|---------------|
| `/`                             | Home / hero            | No            |
| `/properties/`                  | Browse / filter        | No            |
| `/properties/new/`              | Create listing         | Yes           |
| `/properties/mine/`             | My listings            | Yes           |
| `/properties/<slug>/`           | Property detail        | No            |
| `/properties/<slug>/delete/`    | Remove listing         | Yes (owner)   |
| `/dashboard/`                   | Account dashboard      | Yes           |
| `/accounts/profile/edit/`       | Edit profile           | Yes           |
| `/partnerships/`                | Partnership landing    | No            |
| `/partnerships/apply/`          | Apply form             | Yes           |
| `/partnerships/status/`         | My applications        | Yes           |
| `/accounts/login/`              | Sign in                | No            |
| `/accounts/signup/`             | Create account         | No            |
| `/accounts/logout/`             | Sign out               | Yes           |
| `/accounts/password/reset/`     | Forgot password        | No            |
| `/admin/`                       | Django admin           | Staff only    |

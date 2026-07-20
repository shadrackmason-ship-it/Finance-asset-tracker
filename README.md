# MasonTrack

A personal finance and trading tool for traders and investors. Track your portfolio, manage assets, calculate trade risk, and view live market charts.

---

## Features

- Portfolio dashboard with real-time P&L, cost basis, and return percentage
- Risk calculator — position size, money at risk, stop-loss distance, R:R ratio
- Live TradingView charts with RSI, MACD, and 100+ indicators
- Asset allocation chart showing portfolio breakdown
- Transaction history — buy, sell, deposit, withdrawal with full audit trail
- 50+ world currencies (USD, EUR, NGN, KES, ZAR, INR, BRL and more)
- 55+ timezones — all timestamps in your local timezone
- Brute-force lockout, CSRF protection, CSP headers, rate limiting
- Global market coverage — Crypto, Forex, Stocks, Commodities, Indices
- REST API with JWT authentication

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0 + Django REST Framework |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Web Server | Nginx + Gunicorn |
| Charts | TradingView Widgets + Chart.js |
| Deployment | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| Security | django-axes, django-csp, django-honeypot |

---

## Quick Start (Local)

```bash
git clone https://github.com/shadrackmason-ship-it/Finance-asset-tracker.git
cd Finance-asset-tracker

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env with your settings

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000

---

## Deploy with Docker

```bash
git clone https://github.com/shadrackmason-ship-it/Finance-asset-tracker.git
cd Finance-asset-tracker
sudo bash deploy.sh
```

The stack starts four services:

- **frontend** — Nginx on port 80, serves static files and proxies to backend
- **backend** — Django + Gunicorn on port 8000
- **database** — PostgreSQL 16
- **redis** — Redis 7 for sessions and rate limiting

---

## Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=masontrack_db
DB_USER=masontrack
DB_PASSWORD=your-db-password
DB_HOST=database
DB_PORT=5432

CACHE_BACKEND=django.core.cache.backends.redis.RedisCache
REDIS_URL=redis://redis:6379/1

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## REST API

All API endpoints require a JWT token. Get one first:

```
POST /api/auth/token/
{ "username": "you", "password": "yourpassword" }
```

Then pass the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /api/auth/token/ | Get JWT access + refresh tokens |
| POST | /api/auth/refresh/ | Refresh access token |
| GET, POST | /api/assets/ | List or create assets |
| GET, PUT, DELETE | /api/assets/{id}/ | Retrieve, update, or delete an asset |
| GET, POST | /api/transactions/ | List or log transactions |
| GET, PUT, DELETE | /api/transactions/{id}/ | Retrieve, update, or delete a transaction |
| GET, POST | /api/journal/ | List or create journal entries |
| GET, PUT, DELETE | /api/journal/{id}/ | Retrieve, update, or delete a journal entry |
| GET, POST | /api/watchlist/ | List or add watchlist items |
| GET, DELETE | /api/watchlist/{id}/ | Retrieve or remove a watchlist item |
| GET | /api/portfolio/ | Full portfolio summary with P&L |

---

## Risk Calculator

```
Position Size = (Account Balance x Risk %) / Stop-Loss Distance
```

---

## Security

- Brute-force lockout after 5 failed login attempts (django-axes)
- Rate limiting on login and register endpoints
- CSRF protection on all forms
- Content Security Policy headers (django-csp)
- Row-level data isolation — users can only see their own data
- Honeypot traps for bots hitting fake admin URLs
- Audit logging for all security events

---

## Running Tests

```bash
python manage.py test --verbosity=2
```

Tests cover authentication, all 5 API schemes, row-level isolation, and user registration/login/profile.

---

## CI/CD

GitHub Actions runs on every push to `main`:

1. Runs all Django tests against a real PostgreSQL instance
2. Builds and pushes the backend Docker image to GitHub Container Registry
3. Builds and pushes the frontend Docker image to GitHub Container Registry
4. SSHs into the production server and runs `docker compose up`

Required GitHub secrets:

| Secret | Description |
|--------|-------------|
| DEPLOY_HOST | IP address or domain of your server |
| DEPLOY_USER | SSH username on the server |
| DEPLOY_SSH_KEY | Private SSH key for the server |

---

## Project Docs

- [Architecture Diagram](docs/ARCHITECTURE.md)
- [Kanban Board](docs/KANBAN.md)

---

## License

MIT License

---

## Author

Built by [shadrackmason-ship-it](https://github.com/shadrackmason-ship-it)

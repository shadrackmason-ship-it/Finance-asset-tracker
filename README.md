# MasonTrack — Finance & Trading App

A professional personal finance and trading tool built for traders and investors worldwide. Track your portfolio, manage assets, calculate trade risk, and view live market charts — all in one place.

!Python, Django, Docker, License

---

## Features

- **Portfolio Dashboard** — Track all your assets with real-time P&L, cost basis, and return %
- **Risk Calculator** — Calculate position size, money at risk, stop-loss distance, and R:R ratio before every trade
- **Live TradingView Charts** — Full interactive charts with RSI, MACD, and 100+ indicators
- **Asset Allocation Chart** — Visual doughnut chart showing your portfolio breakdown
- **Transaction History** — Log every buy, sell, deposit, and withdrawal with full audit trail
- **50+ World Currencies** — USD, EUR, NGN, KES, ZAR, INR, BRL and more
- **55+ Timezones** — All timestamps in your local timezone
- **Bank-Grade Security** — Brute-force lockout, CSRF protection, CSP headers, rate limiting
- **Global Market Coverage** — Crypto, Forex, Stocks, Commodities, Indices

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0 |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Web Server | Nginx + Gunicorn |
| Charts | TradingView Widgets + Chart.js |
| Deployment | Docker + Docker Compose |
| Security | django-axes, django-csp, django-honeypot |

---

## Quick Start (Local)

```bash
# 1. Clone the repo
git clone https://github.com/shadrackmason-ship-it/Finance-asset-tracker.git
cd Finance-asset-tracker

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env
# Edit .env with your settings

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

Open **http://127.0.0.1:8000**

---

## Deploy with Docker

```bash
# 1. Clone the repo on your server
git clone https://github.com/shadrackmason-ship-it/Finance-asset-tracker.git
cd Finance-asset-tracker

# 2. Run the deploy script
sudo bash deploy.sh
```

App will be live at **http://your-server-ip**

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
DB_HOST=db
DB_PORT=5432

CACHE_BACKEND=django.core.cache.backends.redis.RedisCache
REDIS_URL=redis://redis:6379/1

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

---

## Risk Calculator

The built-in risk calculator helps traders:

- Know exactly **how much money to risk** per trade
- Calculate the correct **position size** based on account balance
- See the **Risk:Reward ratio** before entering a trade
- Visualize **losing streak impact** on their account
- View a **live TradingView chart** for the selected asset

**Formula used:**
```
Position Size = (Account Balance × Risk %) ÷ Stop-Loss Distance
```

---

## Screenshots

| Dashboard | Risk Calculator | Market |
|---|---|---|
| Portfolio overview with P&L | Position sizing tool | Live TradingView charts |

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

## License

MIT License — free to use, modify, and distribute.

---

## Author

Built by [shadrackmason-ship-it](https://github.com/shadrackmason-ship-it)

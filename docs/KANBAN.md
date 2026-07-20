# Kanban Board — MasonTrack

---

## Backlog

| ID | Task | Area |
|----|------|------|
| B-01 | Password reset via email | Auth |
| B-02 | API filtering and search on transactions | API |
| B-03 | Per-user API rate limiting | API |
| B-04 | Staging environment setup | DevOps |
| B-05 | Export portfolio to CSV | Feature |

---

## In Progress

| ID | Task | Area | Assigned |
|----|------|------|----------|
| P-01 | Write additional edge-case tests | Testing | Mason |

---

## Done

| ID | Task | Area |
|----|------|------|
| D-01 | Custom User model — currency, timezone, country | Auth |
| D-02 | Session login with username or email | Auth |
| D-03 | Brute-force lockout — django-axes, 5 attempt limit | Auth |
| D-04 | CSRF protection on all forms | Auth |
| D-05 | Content Security Policy headers — django-csp | Auth |
| D-06 | Honeypot traps on fake admin and login URLs | Auth |
| D-07 | JWT authentication — djangorestframework-simplejwt | Auth/API |
| D-08 | Row-level data isolation on all views and API | Auth |
| D-09 | Asset model and CRUD views | Backend |
| D-10 | Transaction model and CRUD views | Backend |
| D-11 | Trade Journal model and CRUD views | Backend |
| D-12 | Watchlist model and CRUD views | Backend |
| D-13 | Portfolio dashboard with P&L calculation | Backend |
| D-14 | Risk calculator | Backend |
| D-15 | TradingView chart integration | Frontend |
| D-16 | Asset allocation chart — Chart.js | Frontend |
| D-17 | PostgreSQL 16 database | Database |
| D-18 | Redis 7 cache | Database |
| D-19 | Dockerfile — backend (Python 3.12 + Gunicorn) | DevOps |
| D-20 | Dockerfile.frontend — Nginx image | DevOps |
| D-21 | docker-compose.yml — frontend, backend, database, redis | DevOps |
| D-22 | Nginx config — static files + proxy to backend | DevOps |
| D-23 | deploy.sh — one-command server deployment | DevOps |
| D-24 | GitHub Actions — test job with real PostgreSQL | CI/CD |
| D-25 | GitHub Actions — build and push backend Docker image | CI/CD |
| D-26 | GitHub Actions — build and push frontend Docker image | CI/CD |
| D-27 | GitHub Actions — SSH deploy to production server | CI/CD |
| D-28 | djangorestframework installed and configured | API |
| D-29 | Scheme 1 — /api/assets/ full CRUD | API |
| D-30 | Scheme 2 — /api/transactions/ full CRUD | API |
| D-31 | Scheme 3 — /api/journal/ full CRUD | API |
| D-32 | Scheme 4 — /api/watchlist/ full CRUD | API |
| D-33 | Scheme 5 — /api/portfolio/ P&L summary | API |
| D-34 | Unit tests — all 5 API schemes | Testing |
| D-35 | Unit tests — auth, login, registration, profile | Testing |
| D-36 | System architecture diagram — Mermaid | Docs |
| D-37 | Kanban board | Docs |
| D-38 | README — setup, API reference, deployment guide | Docs |

---

## Delivery Checklist

| # | Requirement | Status |
|---|-------------|--------|
| 1 | Authentication and Authorization | Done |
| 2 | Django REST API | Done |
| 3 | At least 5 API schemes | Done — 5 schemes |
| 4 | Dockerized — frontend, backend, database | Done |
| 5 | GitHub Actions — CI + deploy frontend and backend | Done |
| 6 | Kanban board | Done |
| 7 | System diagram | Done |

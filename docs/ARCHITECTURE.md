# System Architecture

## Overview

MasonTrack is a containerized Django application split into four Docker services:
- **frontend** — Nginx on port 80, serves static files and proxies requests to the backend
- **backend** — Django + Gunicorn on port 8000, handles all business logic and API
- **database** — PostgreSQL 16, stores all application data
- **redis** — Redis 7, handles sessions, rate limiting, and brute-force lockout cache

---

## Architecture Diagram

```mermaid
graph TB
    subgraph Client
        B[Browser / API Client]
    end

    subgraph Docker Compose
        subgraph frontend
            N[Nginx :80]
        end

        subgraph backend
            G[Gunicorn :8000]
            DJ[Django Application]
            G --> DJ
        end

        subgraph database
            PG[(PostgreSQL :5432)]
        end

        subgraph cache
            RD[(Redis :6379)]
        end
    end

    B -->|HTTP :80| N
    N -->|Proxy /app/ and /api/| G
    N -->|Serve /static/ directly| N
    DJ -->|ORM queries| PG
    DJ -->|Sessions, rate limiting, axes| RD
```

---

## Request Flow

```mermaid
sequenceDiagram
    participant User
    participant Nginx
    participant Django
    participant PostgreSQL
    participant Redis

    User->>Nginx: GET /app/dashboard/
    Nginx->>Django: Proxy request
    Django->>Redis: Check session
    Redis-->>Django: Session valid
    Django->>PostgreSQL: Query assets + transactions
    PostgreSQL-->>Django: Return rows
    Django-->>Nginx: Rendered HTML response
    Nginx-->>User: HTTP 200

    User->>Nginx: POST /api/auth/token/
    Nginx->>Django: Proxy request
    Django->>PostgreSQL: Verify credentials
    PostgreSQL-->>Django: User record found
    Django-->>Nginx: JWT access + refresh tokens
    Nginx-->>User: 200 OK with tokens
```

---

## API Schemes

All endpoints below require a JWT Bearer token except `/api/auth/token/` and `/api/auth/refresh/`.

```mermaid
graph TD
    Client -->|POST username+password| T[/api/auth/token/]
    T -->|Returns JWT access + refresh| Client

    Client -->|Bearer token| S1[Scheme 1: /api/assets/]
    Client -->|Bearer token| S2[Scheme 2: /api/transactions/]
    Client -->|Bearer token| S3[Scheme 3: /api/journal/]
    Client -->|Bearer token| S4[Scheme 4: /api/watchlist/]
    Client -->|Bearer token| S5[Scheme 5: /api/portfolio/]

    S1 -->|CRUD| DB1[(Assets Table)]
    S2 -->|CRUD| DB2[(Transactions Table)]
    S3 -->|CRUD| DB3[(TradeJournal Table)]
    S4 -->|CRUD| DB4[(Watchlist Table)]
    S5 -->|Read-only P&L summary| DB1
    S5 --> DB2
```

| Scheme | URL | Methods | Description |
|--------|-----|---------|-------------|
| 1 | /api/assets/ | GET, POST, PUT, DELETE | Manage portfolio assets |
| 2 | /api/transactions/ | GET, POST, PUT, DELETE | Log and view transactions |
| 3 | /api/journal/ | GET, POST, PUT, DELETE | Trade journal entries |
| 4 | /api/watchlist/ | GET, POST, DELETE | Watchlist management |
| 5 | /api/portfolio/ | GET | Full P&L portfolio summary |

---

## Database Schema

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string email
        string password
        string preferred_currency
        string timezone
        string country
        bool is_premium
        datetime premium_since
    }

    ASSET {
        int id PK
        int user_id FK
        string name
        string asset_type
        decimal current_price
        string tv_symbol
        datetime created_at
        datetime updated_at
    }

    TRANSACTION {
        int id PK
        int user_id FK
        int asset_id FK
        string transaction_type
        decimal quantity
        decimal price_at_time
        datetime date
        text notes
    }

    TRADEJOURNAL {
        int id PK
        int user_id FK
        string symbol
        string direction
        decimal entry_price
        decimal exit_price
        decimal stop_loss
        decimal take_profit
        decimal lot_size
        string outcome
        decimal pnl
        decimal rr_ratio
        text setup_notes
        text lesson
        datetime date
    }

    WATCHLIST {
        int id PK
        int user_id FK
        string symbol
        string tv_symbol
        string notes
        datetime added_at
    }

    USER ||--o{ ASSET : owns
    USER ||--o{ TRANSACTION : logs
    USER ||--o{ TRADEJOURNAL : records
    USER ||--o{ WATCHLIST : tracks
    ASSET ||--o{ TRANSACTION : has
```

---

## Deployment Pipeline

```mermaid
graph LR
    Dev[Push to main] --> GH[GitHub Actions]
    GH --> T[Job 1: Run Tests]
    T -->|All tests pass| B[Job 2: Build Docker Images]
    T -->|Any test fails| X[Pipeline stops]
    B --> BE[Push backend image to GHCR]
    B --> FE[Push frontend image to GHCR]
    BE --> D[Job 3: SSH Deploy]
    FE --> D
    D --> Pull[docker compose pull]
    Pull --> Up[docker compose up -d]
    Up --> M[Run migrations]
    M --> Live[Live on production server]
```

---

## Security Layers

```mermaid
graph TD
    Request[Incoming Request] --> CSP[Content Security Policy]
    CSP --> CSRF[CSRF Protection]
    CSRF --> RL[Rate Limiting]
    RL --> HP[Honeypot Check]
    HP --> AX[django-axes Brute-force Check]
    AX --> Auth[Authentication - Session or JWT]
    Auth --> Row[Row-level Isolation - user filter on every query]
    Row --> View[View / API Handler]
```

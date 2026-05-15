# HappySR — Senior Resource Web Application

A mobile-responsive web application designed as a comprehensive resource center for seniors, covering health, community activities, finance, travel, learning, and personal expense/investment tracking.

## Features

- **Home** — Latest announcements and upcoming community events
- **Calendar** — Interactive monthly calendar with color-coded event markers
- **Activities** — Community events filterable by category (dancing, yoga, arts, etc.)
- **Learning** — Free online courses, libraries, and senior-focused education programs
- **Health** — Medicare, Medicaid, dental, vision, and mental health resources
- **Technology** — Beginner guides, online safety tips, and useful apps for seniors
- **Travel** — Senior discounts, cruise resources, and trip planning tools
- **Finance** — Social Security, retirement planning, benefits assistance, and fraud protection
- **Expense Tracker** — Log and categorize personal expenses
- **Investment Tracker** — Track portfolio holdings across institutions
- **Reports** — Visual expense reports with pie and bar charts
- **Admin Panel** — User management and role assignment

### Multi-Language Support

English · Español · 简体中文 · 繁體中文 · Tiếng Việt · 한국어

### Authentication

Email/password registration and login with JWT-based session management. Guest users can browse all public pages; registered users unlock personal tracking features; admins can manage users and add events.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Vite, Tailwind CSS |
| Backend | Node.js, Express |
| Database | MySQL 8 |
| Auth | JWT, bcryptjs |
| Charts | Recharts |
| i18n | i18next, react-i18next |
| Calendar | react-calendar |

---

## Getting Started

### Prerequisites

- Node.js 18+
- MySQL 8

### 1. Clone the repo

```bash
git clone https://github.com/sea2sky199/happysr.git
cd happysr
```

### 2. Set up the database

```bash
mysql -u root -p < database/schema.sql
```

### 3. Configure the backend

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env`:

```
PORT=3001
DB_HOST=localhost
DB_USER=root
DB_PASS="your_password"
DB_NAME=happysr
JWT_SECRET=your_long_random_secret
```

> Note: If your password contains `#`, wrap it in double quotes in the `.env` file.

### 4. Install dependencies

```bash
cd backend && npm install
cd ../frontend && npm install
```

### 5. Start the servers

```bash
# Terminal 1 — backend (port 3001)
cd backend && npm run dev

# Terminal 2 — frontend (port 5173)
cd frontend && npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

### 6. Create the first admin

Register an account through the UI, then promote it via MySQL:

```bash
mysql -u root -p -e "UPDATE happysr.users SET role='admin' WHERE email='your@email.com';"
```

---

## Project Structure

```
happysr/
├── frontend/               # React + Vite SPA
│   └── src/
│       ├── components/     # Layout and common UI components
│       ├── context/        # AuthContext, LanguageContext
│       ├── i18n/           # Translation files (en, es, zh-CN, zh-TW, vi, ko)
│       ├── pages/          # One file per route
│       └── utils/api.js    # Axios instance with auth interceptor
├── backend/                # Express REST API
│   └── src/
│       ├── config/         # MySQL connection pool
│       ├── controllers/    # Business logic
│       ├── middleware/     # JWT auth, admin guard
│       └── routes/         # Route definitions
└── database/
    └── schema.sql          # MySQL DDL
```

## API Overview

All endpoints are prefixed with `/api/v1`.

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| POST | `/auth/register` | public | Create account |
| POST | `/auth/login` | public | Sign in, receive JWT |
| GET/PUT | `/users/me` | user | View/update profile |
| GET | `/activities` | public | List upcoming activities |
| POST/DELETE | `/activities/:id` | admin | Manage activities |
| GET | `/calendar` | public | Merged activities + calendar events |
| POST/DELETE | `/calendar/:id` | admin | Manage calendar events |
| GET/POST/DELETE | `/expenses` | user | Expense tracking |
| GET/POST/DELETE | `/investments` | user | Investment tracking |
| GET | `/reports/expenses` | user | Expense summary by category & month |
| GET | `/admin/users` | admin | List all users |
| PUT | `/admin/users/:id/role` | admin | Change user role |

## License

MIT

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Dev Commands

```bash
# Database — run once to create tables
mysql -u root -p < database/schema.sql

# Backend (port 3001)
cd backend
cp .env.example .env   # fill in DB_* and JWT_SECRET
npm run dev            # nodemon server.js

# Frontend (port 5173, proxies /api → localhost:3001)
cd frontend
npm run dev

# Build frontend for production
cd frontend && npm run build
```

## Architecture

Full-stack senior resource web app with role-based access (user / admin).

```
happysr/
├── frontend/       React + Vite + Tailwind — SPA
├── backend/        Node.js + Express — REST API
└── database/       schema.sql — MySQL DDL
```

### Backend (`backend/src/`)

- `config/database.js` — `mysql2` connection pool (reads `DB_*` env vars)
- `middleware/auth.js` — verifies Bearer JWT, attaches `req.user`
- `middleware/admin.js` — guards routes to `role === 'admin'`
- `controllers/` + `routes/` — paired by feature: `auth`, `users`, `activities`, `expenses`, `investments`, `reports`
- All routes mounted under `/api/v1` in `app.js`
- Consistent response shape: `{ success: true, data: ... }` / `{ success: false, error: "..." }`

### Frontend (`frontend/src/`)

- `main.jsx` — wraps app in `<LanguageProvider>` → `<AuthProvider>` → `<BrowserRouter>`
- `context/AuthContext.jsx` — JWT + user stored in `localStorage`; exposes `login`, `register`, `logout`, `refreshUser`, `isAdmin`
- `context/LanguageContext.jsx` — initialises `i18next` with EN/ES JSON; `setLang()` persists choice
- `utils/api.js` — Axios instance; request interceptor injects token; 401 redirects to `/login`
- `App.jsx` — route tree; `<RequireAuth>` and `<RequireAdmin>` wrappers for protected routes
- `components/layout/` — `Header`, `MobileNav` (bottom tab bar on mobile), `Footer`
- `components/common/` — `Card`, `Button`, `Modal`
- `i18n/en.json` and `i18n/es.json` — all UI strings (add keys here when adding UI copy)

### Pages

| Route | Auth | Description |
|-------|------|-------------|
| `/` | public | Home with announcements and latest activities |
| `/health` | public | Medicare/Medicaid/dental/mental health resource links |
| `/activities` | public (admin can add) | Upcoming community events with category filter |
| `/travel` | public | Senior travel resources and cruise links |
| `/login`, `/register` | public | Email/password auth |
| `/dashboard` | user | Profile editor + summary cards |
| `/expenses` | user | Add/delete expenses; running total |
| `/investments` | user | Add/delete investments; portfolio total |
| `/reports` | user | Pie + bar charts of expenses via `recharts` |
| `/admin/users` | admin | Role management table |

### Database tables

`users`, `activities`, `expenses`, `investments`, `calendar_events` — see `database/schema.sql` for full DDL.

### Adding a new feature

1. Add table to `database/schema.sql`
2. Create `backend/src/controllers/<feature>.controller.js` + `routes/<feature>.routes.js`
3. Mount route in `backend/src/app.js`
4. Add i18n strings to `frontend/src/i18n/en.json` and `es.json`
5. Create `frontend/src/pages/<Feature>.jsx`
6. Add route in `frontend/src/App.jsx`
7. Add nav link in `Header.jsx` and optionally `MobileNav.jsx`

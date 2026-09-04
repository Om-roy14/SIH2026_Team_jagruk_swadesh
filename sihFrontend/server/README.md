# Jagruk Swadesh — Auth API

Minimal Express + MongoDB backend that powers real login/signup for the
Jagruk Swadesh frontend (replaces the previous fake, frontend-only auth).

## Setup

1. `cd server`
2. `npm install`
3. `cp .env.example .env` and fill in:
   - `MONGODB_URI` — from MongoDB Atlas (free tier is fine) or a local `mongod`
   - `JWT_SECRET` — any long random string
4. `npm run dev` (or `npm start`) — server runs on `http://localhost:5000`

## Endpoints

| Method | Path              | Body                              | Notes                          |
|--------|-------------------|------------------------------------|---------------------------------|
| POST   | /api/auth/signup  | `{ fullName, email, password }`    | Creates a user, returns token   |
| POST   | /api/auth/login   | `{ email, password }`              | Verifies credentials, returns token |
| GET    | /api/auth/me      | — (Authorization: Bearer `<token>`)| Returns the current user        |

Passwords are hashed with bcrypt before being stored — the plaintext
password is never saved or returned.

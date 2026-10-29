# FastAPI JWT Authentication API

A beginner-friendly authentication API built with Python, FastAPI, SQLite, and JWT. This project demonstrates user registration, password hashing, login, access token generation, and a protected endpoint.

## Features
- User registration with input validation
- Password hashing and verification using pwdlib
- SQLite database for user records
- JWT access token generation using PyJWT
- Token expiration and validation
- Protected `/me` endpoint using HTTP Bearer authentication
- HTTP error handling for invalid credentials and duplicate usernames
- Interactive API testing with Swagger UI

## Tech Stack
- Python
- FastAPI
- SQLite
- Pydantic
- PyJWT
- pwdlib
- python-dotenv
- Uvicorn

## Installation
```bash
git clone YOUR_REPOSITORY_URL
cd fastapi-jwt-authentication
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:
```bash
pip install fastapi uvicorn PyJWT pwdlib python-dotenv
```

## Environment Variables
Create a `.env` file:
```env
SECRET_KEY=your-strong-random-secret-key
```
Never commit the real `.env` file to GitHub.

## Run the Application
```bash
uvicorn main:app --reload
```
Open Swagger UI at `http://127.0.0.1:8000/docs`.

## API Endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/register` | Register a user |
| POST | `/login` | Verify credentials and generate a JWT |
| GET | `/me` | Validate the Bearer token and return the user ID |

## Authentication Flow
1. Register a user.
2. Log in with the registered credentials.
3. Receive a JWT access token.
4. Authorize requests using the Bearer token.
5. Access the protected `/me` endpoint.

## Learning Outcomes
Practical experience with authentication workflows, password security basics, JWT validation, FastAPI dependencies, and protected API endpoints.

## Future Improvements
- Add pytest integration tests.
- Verify the authenticated user still exists in the database.
- Add token revocation or refresh-token handling if required.
- Improve configuration and database connection management.

## Disclaimer
This is a learning project, not a complete production-ready authentication system.

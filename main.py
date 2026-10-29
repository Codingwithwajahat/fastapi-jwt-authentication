
import jwt
import os
import sqlite3
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from pwdlib import PasswordHash

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    raise ValueError("SECRET_KEY is missing from .env")

algorithm = "HS256"

password_hash = PasswordHash.recommended()
security = HTTPBearer()
app = FastAPI()

connection = sqlite3.connect("user.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        hashed_password TEXT NOT NULL
    )
""")

connection.commit()
connection.close()


class Register(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=8, max_length=20)


class Login(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=1, max_length=20)


def auth(token):
    try:
        decoded = jwt.decode(
            token,
            secret_key,
            algorithms=[algorithm]
        )

        user_id = decoded.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: user ID missing"
            )

        return user_id

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


@app.get("/me")
def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    user_id = auth(credentials.credentials)

    return {
        "user_id": user_id
    }


@app.post("/register", status_code=201)
def register(detail: Register):
    connection = sqlite3.connect("user.db")
    cursor = connection.cursor()

    hashed_password = password_hash.hash(detail.password)

    try:
        cursor.execute(
            """
            INSERT INTO users (username, hashed_password)
            VALUES (?, ?)
            """,
            (detail.username, hashed_password)
        )

        user_id = cursor.lastrowid
        connection.commit()

        return {
            "id": user_id,
            "username": detail.username
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    finally:
        connection.close()


@app.post("/login")
def login(detail: Login):
    connection = sqlite3.connect("user.db")
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id, username, hashed_password
            FROM users
            WHERE username = ?
            """,
            (detail.username,)
        )

        user = cursor.fetchone()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        stored_hash = user[2]

        is_valid = password_hash.verify(
            detail.password,
            stored_hash
        )

        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )

        payload = {
            "sub": str(user[0]),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
        }

        token = jwt.encode(
            payload,
            secret_key,
            algorithm=algorithm
        )

        return {
            "message": "Login successful",
            "id": user[0],
            "username": user[1],
            "access_token": token,
            "token_type": "bearer"
        }

    finally:
        connection.close()
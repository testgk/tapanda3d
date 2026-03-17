import hashlib
import os
import secrets
import sqlite3

_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'users.db')


# ---------------------------------------------------------------------------
# Database initialisation
# ---------------------------------------------------------------------------

def init_db() -> None:
    """Create the users table if it does not exist yet."""
    with _connect() as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS users (
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname           TEXT    UNIQUE NOT NULL,
                email              TEXT    UNIQUE NOT NULL,
                password_hash      TEXT    NOT NULL,
                verified           INTEGER NOT NULL DEFAULT 0,
                verification_token TEXT
            )
            '''
        )
        conn.commit()


# ---------------------------------------------------------------------------
# Password helpers
# ---------------------------------------------------------------------------

def _hash_password(password: str) -> str:
    """Return a salted PBKDF2-HMAC-SHA256 hash of *password*."""
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 200_000)
    return salt.hex() + ':' + dk.hex()


def _generate_token() -> str:
    """Return a random 6-character uppercase alphanumeric verification code."""
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(secrets.choice(alphabet) for _ in range(6))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_user(nickname: str, email: str, password: str) -> str:
    """
    Insert a new (unverified) user and return the verification token.

    Raises ValueError if the nickname or email is already registered.
    """
    token = _generate_token()
    password_hash = _hash_password(password)
    with _connect() as conn:
        try:
            conn.execute(
                '''
                INSERT INTO users
                    (nickname, email, password_hash, verified, verification_token)
                VALUES (?, ?, ?, 0, ?)
                ''',
                (nickname, email, password_hash, token),
            )
            conn.commit()
        except sqlite3.IntegrityError as exc:
            msg = str(exc).lower()
            if 'nickname' in msg:
                raise ValueError('Nickname is already taken.') from exc
            if 'email' in msg:
                raise ValueError('Email is already registered.') from exc
            raise
    return token


def verify_email(token: str) -> bool:
    """
    Mark the user associated with *token* as verified.

    Returns True on success, False if the token is unknown.
    """
    with _connect() as conn:
        cur = conn.execute(
            'SELECT id FROM users WHERE verification_token = ?', (token,)
        )
        row = cur.fetchone()
        if row is None:
            return False
        conn.execute(
            'UPDATE users SET verified = 1, verification_token = NULL WHERE id = ?',
            (row[0],),
        )
        conn.commit()
    return True


def nickname_exists(nickname: str) -> bool:
    with _connect() as conn:
        cur = conn.execute(
            'SELECT id FROM users WHERE nickname = ?', (nickname,)
        )
        return cur.fetchone() is not None


def email_exists(email: str) -> bool:
    with _connect() as conn:
        cur = conn.execute(
            'SELECT id FROM users WHERE email = ?', (email,)
        )
        return cur.fetchone() is not None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _connect() -> sqlite3.Connection:
    return sqlite3.connect(_DB_PATH)

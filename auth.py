"""
Authentication helpers: password hashing/verification and session-based
auth guards for FastAPI routes.

Uses PBKDF2-HMAC-SHA256 (stdlib `hashlib`) for password hashing so the
project has zero compiled-dependency friction (no bcrypt build step)
while still being a strong, salted, industry-standard KDF.
"""
import hashlib
import hmac
import os

from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from models import User

PBKDF2_ITERATIONS = 260_000


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"{salt.hex()}${dk.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt_hex, hash_hex = stored_hash.split("$")
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(hash_hex)
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return hmac.compare_digest(expected, actual)


def get_current_user(request: Request, db: Session):
    """Return the logged-in User, or None."""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


def login_required(request: Request, db: Session):
    """
    Returns a RedirectResponse to /login if the visitor is not
    authenticated, otherwise returns the User object.
    """
    user = get_current_user(request, db)
    if not user:
        return None
    return user


def require_auth_redirect() -> RedirectResponse:
    return RedirectResponse(url="/login", status_code=303)

"""Chapter 8: API keys, and bearer tokens (JWT) with scopes.

Run:   fastapi dev library_auth.py
Try:   curl -i http://127.0.0.1:8000/partner/books -H "X-API-Key: demo-key-123"
       curl -s -X POST http://127.0.0.1:8000/token -d "username=ada&password=lovelace&scope=books:read books:write"

Note: the /token endpoint uses the OAuth 2.0 "password" grant because it fits in one file.
It is a teaching shortcut: OAuth 2.1 removes that grant, and real systems get tokens from an
authorization server with the authorization code flow and PKCE (see the chapter).
"""
import hashlib
import hmac
import os
import time

import jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from pydantic import BaseModel

app = FastAPI(title="Library API with authentication")

# ---------------------------------------------------------------- configuration
SECRET_KEY = os.environ.get("LIBRARY_SECRET", "dev-only-secret-change-me-0123456789abcdef")
ALGORITHM = "HS256"
ISSUER = "https://auth.library.example"
AUDIENCE = "library-api"
TOKEN_TTL = 15 * 60          # seconds: keep access tokens short-lived


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# Store only hashes of API keys, never the keys themselves
API_KEYS = {sha256("demo-key-123"): "partner-bookshop"}


def hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1)


def make_user(password: str, scopes: list[str]) -> dict:
    salt = os.urandom(16)
    return {"salt": salt, "hash": hash_password(password, salt), "scopes": scopes}


USERS = {
    "ada": make_user("lovelace", ["books:read", "books:write"]),
    "bob": make_user("builder", ["books:read"]),
}

BOOKS = [{"id": 1, "title": "Dune"}, {"id": 2, "title": "Emma"}]


# ---------------------------------------------------------------- API key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(key: str | None = Depends(api_key_header)) -> str:
    client = API_KEYS.get(sha256(key)) if key else None
    if client is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing or invalid API key",
                            headers={"WWW-Authenticate": 'ApiKey realm="library"'})
    return client


# ---------------------------------------------------------------- bearer tokens
oauth2 = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"books:read": "Read books", "books:write": "Create and change books"},
)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    scope: str


@app.post("/token", response_model=Token)
def issue_token(form: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form.username)
    if not user or not hmac.compare_digest(user["hash"], hash_password(form.password, user["salt"])):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong username or password")
    granted = [s for s in (form.scopes or user["scopes"]) if s in user["scopes"]]   # never more than allowed
    now = int(time.time())
    claims = {"iss": ISSUER, "aud": AUDIENCE, "sub": form.username, "iat": now,
              "exp": now + TOKEN_TTL, "scope": " ".join(granted)}
    return Token(access_token=jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM),
                 expires_in=TOKEN_TTL, scope=" ".join(granted))


def current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2)) -> dict:
    challenge = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
    try:
        claims = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],   # pin the algorithm
                            audience=AUDIENCE, issuer=ISSUER)
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired", headers={"WWW-Authenticate": challenge})
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token", headers={"WWW-Authenticate": challenge})
    have = set(claims.get("scope", "").split())
    missing = [s for s in security_scopes.scopes if s not in have]
    if missing:   # authenticated, but not allowed: 403, not 401
        raise HTTPException(403, f"Missing scope: {' '.join(missing)}",
                            headers={"WWW-Authenticate": challenge})
    return claims


# ---------------------------------------------------------------- endpoints
@app.get("/public/books")
def public_books():
    return BOOKS


@app.get("/partner/books")
def partner_books(client: str = Depends(require_api_key)):
    return {"client": client, "books": BOOKS}


@app.get("/me")
def me(user: dict = Security(current_user)):
    return {"user": user["sub"], "scopes": user["scope"].split(), "expires": user["exp"]}


@app.get("/books")
def list_books(user: dict = Security(current_user, scopes=["books:read"])):
    return BOOKS


@app.post("/books", status_code=201)
def add_book(book: dict, user: dict = Security(current_user, scopes=["books:write"])):
    new = {"id": len(BOOKS) + 1, "title": str(book.get("title", "Untitled")), "added_by": user["sub"]}
    BOOKS.append(new)
    return new

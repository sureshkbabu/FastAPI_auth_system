import time
from collections import defaultdict
from fastapi import Request, HTTPException, status

LOGIN_LIMIT = 5          # max attempts
LOGIN_WINDOW = 60        # seconds

_attempts = defaultdict(list)

def login_rate_limiter(request: Request):
    ip = request.client.host
    now = time.time()

    attempts = _attempts[ip]
    attempts = [t for t in attempts if now - t < LOGIN_WINDOW]
    _attempts[ip] = attempts

    if len(attempts) >= LOGIN_LIMIT:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Try again later.",
        )

    attempts.append(now)
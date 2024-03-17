import hashlib
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from . import redis


security = HTTPBasic()


async def login_required(credentials: HTTPBasicCredentials = Depends(security)):
    """
        Authentication
    """
    username = credentials.username
    password = credentials.password

    user_pass = hashlib.sha1(password.encode()).hexdigest()
    right_password = await redis.redis.get_value(username)
    if user_pass == right_password:
        pass
    else:
        raise HTTPException(status_code=401, detail="Permission denied")

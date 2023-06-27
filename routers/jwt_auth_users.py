from fastapi import APIRouter, HTTPException, Depends, status, FastAPI
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET_KEY = "ae994f9cd51aa9f5e0a70c37170859650efabdb2661106c32bba175ef2a97c4e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):
    username: str
    full_name: str
    emai: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "lonchop": {
        "username": "lonchop",
        "full_name": "Orangel Jose",
        "emai": "hola@hola.com",
        "disabled": False,
        "password": "$2a$12$thIMnKlzwumQSzy2Xo/7i.UgRqEvjJtHEsS7xiiw/H/IYUvHDVLM2"
    },
    "lonchop2": {
        "username": "lonchop2",
        "full_name": "Angel Rafael",
        "emai": "hola@hola.com",
        "disabled": True,
        "password": "$2a$12$thIMnKlzwumQSzy2Xo/7i.UgRqEvjJtHEsS7xiiw/H/IYUvHDVLM2"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="No esta autorizado, credenciales invalidas", headers={"www-authenticate": "Bearer"})
    try:
        username = jwt.decode(
            token, SECRET_KEY, algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    user = search_user_db(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta")

    acces_token_expiration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + acces_token_expiration

    access_token = {"sub": user.username, "exp": expire, }

    return {
        "access_token": jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM), "token_type": "bearer"
    }


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

from fastapi import APIRouter, HTTPException, Depends, status, FastAPI
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password": "123"
    },
    "lonchop2": {
        "username": "lonchop2",
        "full_name": "Angel Rafael",
        "emai": "hola@hola.com",
        "disabled": True,
        "password": "321"
    }
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])


def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="No esta autorizado", headers={"www-authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inactivo")
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcta")
    return {
        "access_token": user.username, "token_type": "bearer"
    }


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

from typing import List


router = APIRouter(prefix="/users", tags=["users"],
                   responses={404: {"message": "No encontrado"}})


# class User(BaseModel):  # Con BaseModel me ahorro el tener que hacer la class tradicional de python
#     id: int
#     name: str
#     surname: str
#     url: str
#     age: int


# class User:
#     def __init__(self, id: int, name: str, surname: str, url: str, age: int):
#         self.id = id
#         self.name = name
#         self.surname = surname
#         self.url = url
#         self.age = age


@router.get("", response_model=List[User])
async def users():
    return users_schema(db_client.users.find())


@router.get("/{id}")  # Path se usa cuando es obligatorio
async def user(id: str):
    return search_user("_id", ObjectId(id))


# @router.get("/user")
# async def user(id: str):
#   return search_user("_id", ObjectId(id))


@router.post("", response_model=User, status_code=201)
async def user(user: User):
    # if isinstance(search_user(user.id), User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    # else:
    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**new_user)
    # users_list.append(user)
    # return user


@router.put("")
async def user(user: User):
    try:
        user_dict = dict(user)
        del user_dict["id"]
        db_client.users.find_one_and_replace(
            {"_id": ObjectId(user.id)}, user_dict)

    except:
        return {"No ha encontrado el usuario para actualizarlo"}
#     for indx, save_user in enumerate(users_list):
#         if save_user.id == user.id:
#             users_list[indx] = user
#             found = True
#     else:
    return search_user("_id", ObjectId(user.id))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found:
        return {"No ha encontrado el usuario para elimarlo"}

    # for indx, save_user in enumerate(users_list):
    #     if save_user.id == id:
    #         del users_list[indx]
    #         found = True
    # if not found:
    #     return {"No ha encontrado el usuario para elimarlo"}
    # else:
    #     return user


def search_user(field: str, key):
    # users = filter(lambda user: (user.id == id) and (
    #     user.name.lower() == name.lower()), users_list)
    # users = filter(lambda user: user.id == id, users_list)
    try:
        user = user_schema(db_client.users.find_one({field: key}))
        return User(**user)
        # return list(users)[0]
    except:
        return {"No se ha encontrado el usuario"}

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["products"],
                   responses={404: {"message": "No encontrado"}})

list_products = ["procuct 1", "product 2", "product 3"]


@router.get("")
async def products():
    return list_products


@router.get("/{id}")
async def products(id: int):
    return list_products[id - 1]

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):  # Con BaseModel me ahorro el tener que hacer la class tradicional de python
    id: Optional[str]
    name: str
    surname: str
    email: str
    age: int

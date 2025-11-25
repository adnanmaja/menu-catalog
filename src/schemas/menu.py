from pydantic import BaseModel
from typing import List

class MenuCreate(BaseModel):
    name: str
    category: str
    calories: float
    price: float
    ingredients: List[str]
    description: str


class MenuResponse(BaseModel):
    id: int
    name: str
    category: str
    calories: float
    price: float
    ingredients: List[str]
    description: str


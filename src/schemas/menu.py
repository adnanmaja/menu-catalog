from pydantic import BaseModel
from typing import List, Optional

class MenuCreate(BaseModel):
    name: str
    category: Optional[str] = None
    calories: float
    price: float
    ingredients: List[str]
    description: Optional[str] = None


class MenuResponse(BaseModel):
    id: int
    name: str
    category: str
    calories: float
    price: float
    ingredients: List[str]
    description: str
    alergen: Optional[str] = None


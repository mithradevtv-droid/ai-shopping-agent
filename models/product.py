from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    title: str
    brand: str
    price: int
    rating: Optional[float] = None
    reviews: Optional[int] = None
    source: str
    url: str
    image: Optional[str] = None
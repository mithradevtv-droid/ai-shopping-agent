from pydantic import BaseModel
from typing import List

class UserPreference(BaseModel):
    category: str
    budget: int
    priorities: List[str]
    brand_constraints: List[str]
    
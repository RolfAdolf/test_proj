from typing import Optional
from pydantic import BaseModel


class CategoryRequest(BaseModel):
    name: str
    description: Optional[str]
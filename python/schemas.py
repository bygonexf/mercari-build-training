from typing import List, Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    category_id: int
    image_name: str

class Item(ItemBase):
    id: Optional[int]
    class Config:
        from_attributes = True

class ItemCreate(ItemBase):
    pass

class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    id: Optional[int]
    class Config:
        from_attributes = True

class CategoryCreate(CategoryBase):
    pass
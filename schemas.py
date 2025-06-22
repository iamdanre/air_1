from pydantic import BaseModel, EmailStr
from typing import List, Optional

class CustomerBase(BaseModel):
    name: str
    surname: str
    email: EmailStr

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    class Config:
        orm_mode = True

class ShopItemCategoryBase(BaseModel):
    title: str
    description: Optional[str] = None

class ShopItemCategoryCreate(ShopItemCategoryBase):
    pass

class ShopItemCategory(ShopItemCategoryBase):
    id: int
    class Config:
        orm_mode = True

class ShopItemBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category_ids: List[int] = []

class ShopItemCreate(ShopItemBase):
    pass

class ShopItem(ShopItemBase):
    id: int
    categories: List[ShopItemCategory] = []
    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    shopitem_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    shop_item: ShopItem
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    customer: Customer
    items: List[OrderItem]
    class Config:
        orm_mode = True 
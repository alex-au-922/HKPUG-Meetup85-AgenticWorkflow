from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import Relationship, SQLModel, Field
import sqlalchemy as sa
import uuid
from enum import StrEnum

if TYPE_CHECKING:
    from schema.orders import OrderItem
    
class ProductCategory(StrEnum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    HOME = "home"
    TOYS = "toys"

class Product(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    unit_price: float = Field(nullable=False)
    stock: int = Field(nullable=False)
    sku: str = Field(nullable=False, unique=True)
    is_available: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": sa.func.now})
    category: ProductCategory = Field(default=ProductCategory.ELECTRONICS)
    
    order_items: list["OrderItem"] = Relationship(back_populates="product", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
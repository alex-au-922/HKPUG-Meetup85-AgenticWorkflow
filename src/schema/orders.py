from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import uuid
from enum import StrEnum

if TYPE_CHECKING:
    from schema.customers import Customer
    from schema.products import Product

class OrderStatus(StrEnum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    
class Order(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    customer_id: uuid.UUID = Field(foreign_key="customer.id")
    total_amount: float = Field(nullable=False)
    order_date: datetime = Field(nullable=False, default=datetime.now)
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    
    # Relationships
    customer: "Customer" = Relationship(back_populates="orders")
    order_items: list["OrderItem"] = Relationship(back_populates="order", sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class OrderItem(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    order_id: uuid.UUID = Field(foreign_key="order.id")
    product_id: uuid.UUID = Field(foreign_key="product.id")
    quantity: int = Field(nullable=False)
    
    # Relationships
    order: "Order" = Relationship(back_populates="order_items")
    product: "Product" = Relationship(back_populates="order_items")
    
    @property
    def sub_total(self) -> float:
        return self.quantity * self.product.price if self.product else 0.0
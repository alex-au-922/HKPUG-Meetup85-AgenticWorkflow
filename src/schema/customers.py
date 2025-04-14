from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import uuid
from enum import StrEnum

if TYPE_CHECKING:
    from schema.orders import Order

class CustomerTier(StrEnum):
    BASIC = "basic"
    PREMIUM = "premium"
    VIP = "vip"
    
class Customer(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    phone: str = Field(nullable=True)
    created_at: datetime = Field(default_factory=datetime.now)
    login_date: datetime = Field(default_factory=datetime.now)
    tier: CustomerTier = Field(default=CustomerTier.BASIC)
    
    # Relationships
    orders: list["Order"] = Relationship(back_populates="customer")

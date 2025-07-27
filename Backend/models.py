from beanie import Document, Indexed, Link, BackLink, before_event, Insert, Replace
from beanie import Indexed
from pydantic import Field, BaseModel, field_validator
from typing import List, Dict, Optional
from decimal import Decimal
from datetime import datetime, timezone
from enum import Enum
from pymongo import IndexModel
from decimal import Decimal
from bson.decimal128 import Decimal128
from pydantic import model_validator
from beanie import PydanticObjectId

class TransactionTypeEnum(str, Enum):
    buy = "Buy"
    sell = "Sell"
    credit = "Credit"           
    debit = "Debit"              
    fee = "Fee"               
    reward = "Reward"            
    refund = "Refund"            

class StatusEnum(str, Enum):
    active = "Active"           
    checked_out = "Checked Out"   
    expired = "Expired"        
    cancelled = "Cancelled"      

class OrderStatusEnum(str, Enum):
    buy = "Buy"
    sell = "Sell"
    pending = "Pending"          
    executed = "Executed"        
    cancelled = "Cancelled"      
    failed = "Failed"            

class CreditReasonEnum(str, Enum):
    trade = "Trade"             
    top_up = "Top Up"            
    fee = "Fee"                  
    reward = "Reward"            
    refund = "Refund"            
    adjustment = "Adjustment" 
    deposit = "Deposit"   

class OrderTypeEnum(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class User(Document):
    username: str = Field(..., description="Unique username")
    password_hash: str
    is_active: bool = Field(default=True)
    role: str = Field(default="user")
    credits: Decimal = Field(default=Decimal("0"))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    portfolios: Optional[List[BackLink["Portfolio"]]] = Field(default_factory=list, original_field="user")
    orders: Optional[List[BackLink["Order"]]] = Field(default_factory=list, original_field="user")
    transactions: Optional[List[BackLink["Transaction"]]] = Field(default_factory=list, original_field="user")
    carts: Optional[List[BackLink["Cart"]]] = Field(default_factory=list, original_field="user")
    credits_history: Optional[List[BackLink["CreditsHistory"]]] = Field(default_factory=list, original_field="user")

    @field_validator("credits", mode="before")
    def convert_decimal128(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v

    class Settings:
        name = "users"
        indexes = [
            IndexModel([("username", 1)], unique=True),
            IndexModel([("created_at", -1)]),
            IndexModel([("role", 1)]),
        ]
        
        bson_encoders = {
            Decimal: lambda v: Decimal128(str(v))
        }


class CryptoPair(Document):
    symbol: str = Indexed(unique=True)
    base_asset: str
    quote_asset: str
    status: str

    last_price: Optional[Decimal128] = None
    last_price_time: Optional[datetime] = None
    min_qty: Optional[Decimal128] = None
    step_size: Optional[Decimal128] = None
    tick_size: Optional[Decimal128] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "crypto_pairs"
        indexes = [
            IndexModel([("symbol", 1)], unique=True),
            IndexModel([("base_asset", 1)]),
            IndexModel([("status", 1)])
        ]

    class Config:
        arbitrary_types_allowed = True


class Candle(Document):
    symbol: str
    interval: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal
    candle_time: datetime

    @field_validator("open", "high", "low", "close", "volume", mode="before")
    @classmethod
    def convert_decimal128(cls, value):
        if isinstance(value, Decimal128):
            return Decimal(str(value.to_decimal()))
        return value


    class Settings:
        name = "candles"
        indexes = [
            IndexModel([("symbol", 1), ("candle_time", 1)]),
            IndexModel([("symbol", 1), ("interval", 1), ("candle_time", -1)]),
            IndexModel([("candle_time", -1)])
        ]


class Order(Document):
    user: Link[User]
    symbol: str  
    side: str  
    order_type: str  
    quantity: Decimal
    price: Optional[Decimal] = None
    status: Optional[str] = 'PENDING' 
    order_id: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    executed_at: Optional[datetime] = None
    transactions: Optional[List[BackLink["Transaction"]]] = Field(default_factory=list, original_field="order")

    @field_validator('quantity', 'price', mode='before')
    @classmethod
    def convert_decimal128(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v

    class Settings:
        name = "orders"
        indexes = [
            IndexModel([("user.$id", 1), ("created_at", -1)]),
            IndexModel([("symbol", 1), ("created_at", -1)]),
            IndexModel([("status", 1), ("created_at", -1)]),
            IndexModel([("order_type", 1)]),
            IndexModel([("side", 1)]),
        ]


class Transaction(Document):
    user: Link[User]
    order: Link[Order]
    symbol: str  
    transaction_type: TransactionTypeEnum  
    quantity: Decimal  
    price: Decimal
    total_amount: Decimal  
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="before")
    @classmethod
    def convert_decimal128(cls, values):
        for k, v in values.items():
            if isinstance(v, Decimal128):
                values[k] = v.to_decimal()
        return values

    class Settings:
        name = "transactions"
        indexes = [
            IndexModel([("user.$id", 1), ("created_at", -1)]),
            IndexModel([("symbol", 1), ("created_at", -1)]),
            IndexModel([("order.$id", 1)]),
            IndexModel([("transaction_type", 1), ("created_at", -1)])
        ]

class Portfolio(Document):
    user: Link[User]
    # user_id: PydanticObjectId
    symbol: str
    quantity: Decimal
    avg_buy_price: Decimal
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("quantity", "avg_buy_price", mode="before")
    @classmethod
    def convert_decimal128(cls, value):
        if str(type(value)) == "<class 'bson.decimal128.Decimal128'>":
            return str(value.to_decimal())
        return value

    class Settings:
        name = "portfolios"
        indexes = [
            IndexModel([("user.$id", 1), ("symbol", 1)], unique=True),
            IndexModel([("user.$id", 1)]),
            IndexModel([("updated_at", -1)])
        ]

class CartItemEmbed(BaseModel):
    symbol: str  
    order_type: OrderTypeEnum  
    quantity: Decimal
    price: Decimal

    @field_validator("quantity", "price", mode="before")
    @classmethod
    def convert_decimal128(cls, v):
        if isinstance(v, Decimal128):
            return v.to_decimal()
        return v

    
class Cart(Document):
    user: Link[User]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: StatusEnum
    items: List[CartItemEmbed] = Field(default_factory=list)

    class Settings:
        name = "carts"
        indexes = [
            IndexModel([("user.$id", 1), ("status", 1)]),
            IndexModel([("created_at", -1)]),
            IndexModel([("updated_at", -1)])
        ]

    @before_event(Insert)
    @before_event(Replace)
    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)

class CandleSyncTracker(Document):
    symbol: str
    last_fetched: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "candle_sync_tracker"


class CreditsHistory(Document):
    user: Link[User]
    change_amount: Decimal  
    reason: CreditReasonEnum  
    balance_after: Optional[Decimal] = None  
    metadata: Optional[Dict] = None  
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @model_validator(mode="before")
    @classmethod
    def convert_decimal128(cls, values):
        for k, v in values.items():
            if isinstance(v, Decimal128):
                values[k] = v.to_decimal()
        return values

    class Settings:
        name = "credits_history"
        indexes = [
            IndexModel([("user.$id", 1), ("created_at", -1)]),
            IndexModel([("reason", 1), ("created_at", -1)])
        ]

class Cache(Document):
    key: str = Indexed(unique=True)  
    value: Dict 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime

    class Settings:
        name = "cache"
        indexes = [
            IndexModel([("key", 1)], unique=True),
            IndexModel([("expires_at", 1)], expireAfterSeconds=0) 
        ]

class Transfer(Document):
    from_user: Link[User]                
    to_user: Link[User]                  
    symbol: str = Field(..., min_length=1)       
    amount: Decimal = Field(..., gt=0)           
    timestamp: datetime = Field(default_factory=datetime.now(timezone.utc))
    note: Optional[str] = None                  

    class Settings:
        name = "transfers"

    class Config:
        json_schema_extra = {
            "example": {
                "from_user": "ObjectId",
                "to_user": "ObjectId",
                "symbol": "BTC",
                "amount": "0.5",
                "timestamp": "2025-06-24T10:00:00Z",
                "note": "For coffee"
            }
        }


# #Responses
# class OrderRequest(BaseModel):
#     user_id: str
#     symbol: str
#     side: str          
#     order_type: str    
#     quantity: float
#     price: float = None

class OrderRequest(BaseModel):
    # user_id: str
    symbol: str
    side: str
    quantity: float
    order_type: str
    price: Optional[float] = None

class TransferRequest(BaseModel):
    to_username: str = Field(..., description="Receiver's username")
    symbol: str = Field(..., description="Cryptocurrency symbol (e.g., BTC)")
    amount: Decimal = Field(..., gt=0, description="Amount of crypto to transfer")

    class Config:
        json_schema_extra = {
            "example": {
                "to_username": "johndoe",
                "symbol": "BTC",
                "amount": "0.25"
            }
        }

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str 
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
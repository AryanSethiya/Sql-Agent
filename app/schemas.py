from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# SQL Agent schemas
class SQLQuery(BaseModel):
    query: str
    description: Optional[str] = None

class SQLResponse(BaseModel):
    result: List[Dict[str, Any]]
    query: str
    message: str
    success: bool

class CRUDOperation(BaseModel):
    operation: str  # CREATE, READ, UPDATE, DELETE
    table: str
    data: Dict[str, Any]
    where_clause: Optional[Dict[str, Any]] = None

class CRUDResponse(BaseModel):
    success: bool
    message: str
    affected_rows: Optional[int] = None
    data: Optional[List[Dict[str, Any]]] = None 
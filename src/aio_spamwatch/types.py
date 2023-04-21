from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Permission(str, Enum):
    Root = "Root"
    Admin = "Admin"
    User = "User"


class Token(BaseModel):
    id: int
    permission: Optional[Permission]
    token: str
    user_id: int = Field(alias="userid")
    retired: bool

    class Config:
        use_enum_values = True


class Ban(BaseModel):
    id: int
    reason: str
    date: datetime = Field
    admin: int
    message: Optional[str]

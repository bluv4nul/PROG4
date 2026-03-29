from pydantic import BaseModel, ConfigDict, EmailStr
from models.models import Subscription
from schemas.subscription_schema import SubscriptionRead


class UserCreate(BaseModel):
    username: str
    email: EmailStr


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr


class UserDetailRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: UserRead
    subscriptions: list[SubscriptionRead]


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

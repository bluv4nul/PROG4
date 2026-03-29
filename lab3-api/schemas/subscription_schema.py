from pydantic import BaseModel, ConfigDict


class SubscriptionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    currency_id: int


class SubscriptionCreate(BaseModel):
    user_id: int
    currency_id: int


class SubscriptionDelete(BaseModel):
    user_id: int
    currency_id: int

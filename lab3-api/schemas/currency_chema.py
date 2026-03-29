from pydantic import BaseModel, ConfigDict


class Currency(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    value: float

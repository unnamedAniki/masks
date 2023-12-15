from pydantic import BaseModel


class ClientInfo(BaseModel):
    id: int
    Feature: dict
    product_data: str
    channel_data: str


class ModelOutput(BaseModel):
    id: int
    communication_text: str
    accuracy: float


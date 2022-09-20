from pydantic import BaseModel


class Item(BaseModel):
    deductible: int
    stop_loss: int
    oop_max: int

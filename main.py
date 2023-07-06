from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Trading App"
)

users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "trader", "name": "Mary"},
    {"id": 3, "role": "investor", "name": "Vova "},
    {"id": 4, "role": "trader", "name": "Matt", "degree": [
        {"id": 0, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
    ]}

]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[list[Degree]] = []


@app.get("/users/{user_id}", response_model=list[User])
def get_user(user_id: int):
    return [user for user in users if user.get("id") == user_id]


@app.post("/users/{user_id}")
def change_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, users))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}


trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 1000, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 999, "amount": 2.12},
]


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post("/trades/{new_trade}")
def add_trades(new_trades: list[Trade]):
    trades.extend(new_trades)
    return {"status": 200, "data": trades}

from datetime import datetime
from fastapi import Body, APIRouter
from typing import Union, Optional
from pydantic import BaseModel
from config.database import db


class Reservation(BaseModel):
    user_id: str
    locker_id: int
    backpack: list[str]
    time_select: int
    time_start: datetime
    fee: float
    end_time: datetime


class Locker(BaseModel):
    locker_id: int
    available: bool
    reservation_id: object #object _id


router = APIRouter(prefix="/locker",
                   tags=["locker"])


@router.get("/")
def root():
    return {"msg": "201"}


@router.get("/{locker_id}")
def check_available_locker(locker_id: int):
    pass


@router.post("/create")
def create_reservation_locker(user: Reservation):
    pass


@router.delete("/{user_id}/{money}")
def delete_reservation_locker(user_id: str, money: float):
    pass
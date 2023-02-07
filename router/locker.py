from datetime import datetime, timedelta
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
    end_time: datetime = None


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
    locker = db['locker']
    check_locker = list(locker.find({'locker_id': locker_id}, {"_id": False}))
    if check_locker[0]['available']:
        return {"msg": "This locker is available"}
    else:
        user = db['reservation_locker']
        reservation = list(user.find({'locker_id': locker_id}, {"_id": False}))
        end =  reservation[0]['time_start'] + timedelta(hours=reservation[0]['time_select'])
        return {"msg": "This locker had reservation",
                "end_time": f"{end-datetime.now()} left"}

@router.post("/create")
def create_reservation_locker(reservation: Reservation):
    pass


@router.delete("/{user_id}/{money}")
def delete_reservation_locker(user_id: str, money: float):
    pass
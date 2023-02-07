from datetime import datetime, timedelta
from typing import Optional, Union

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from config.database import db


class Reservation(BaseModel):
    user_id: str
    locker_id: int
    backpack: list[str]
    time_select: int
    time_start: datetime
    fee: float

class Locker(BaseModel):
    locker_id: int
    available: bool
    reservation_id: object #object _id


router = APIRouter(prefix="/locker",
                   tags=["locker"])


@router.get("/")
def root():
    return {"msg": "201"}

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

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
    reserve_collection = db['reservation_locker']
    values = list(reserve_collection.find({"user_id": user_id}, {'_id': False}))
    print(len(values))

    if len(values) == 0:
        raise HTTPException(status_code=404, detail="Reservation not found")
    elif len(values) > 1:
        raise HTTPException(status_code=500, detail="Something went wrong (len > 1)")
    elif len(values) == 1:
        resp = values[0]
        fee = resp['fee']
        time_user = timedelta(hours=resp['time_select'])
        real_time_used = datetime.now() - resp['time_start']

        time_exceed = real_time_used - time_user
        if (time_exceed <= timedelta(0)):
            resp = reserve_collection.delete_one({"user_id": user_id})

            return {'msg': "Delete Success!"}

        else:
            hour_exceed, minute_exceed, second_exceed = days_hours_minutes(time_exceed)
            if (second_exceed > 0):
                minute_exceed += 1
            if (hour_exceed > 0):
                minute_exceed += hour_exceed * 60

            fine = minute_exceed * 2

            total_fee = fee + fine

            if (total_fee > money):
                raise HTTPException(status_code=400, detail="Not enough money")

            else:
                resp = reserve_collection.delete_one({"user_id": user_id})

                return {'msg': "Delete Success!"}


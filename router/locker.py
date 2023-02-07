from datetime import datetime, timedelta
from typing import List, Optional, Union

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from config.database import db


class Reservation(BaseModel):
    user_id: str
    locker_id: int
    backpack: List[str]
    time_select: int
    time_start: datetime = None
    fee: float = 0

class Locker(BaseModel):
    locker_id: int
    available: bool
    reservation_id: object #object _id


router = APIRouter(prefix="/locker",
                   tags=["locker"])


@router.get("/")
def root():
    all_locker = db['locker']
    locker_status = {}
    check = ""
    for locker in list(all_locker.find({}, {"_id": False})):
        if locker['available']:
            check = "available"
        else:
            check = "unavailable"
        locker_status[locker['locker_id']] = check
    return {"locker": locker_status}

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

@router.get("/{locker_id}")
def check_available_locker(locker_id: int):
    locker = db['locker']
    check_locker = list(locker.find({'locker_id': locker_id}, {"_id": False}))
    if len(check_locker) == 0:
        raise HTTPException(status_code=404, detail="Locker not found")
    elif len(check_locker) > 1:
        raise HTTPException(status_code=500, detail=f"Something went wrong (locker {locker_id} > 1)")
    if check_locker[0]['available']:
        return {"msg": "This locker is available"}
    else:
        user = db['reservation_locker']
        reservation = list(user.find({'locker_id': locker_id}, {"_id": False}))
        if len(reservation) == 0:
            raise HTTPException(status_code=404, detail="Reservation not found")
        elif len(reservation) > 1:
            raise HTTPException(status_code=500, detail=f"Something went wrong (locker {locker_id} reservation > 1)")
        end = reservation[0]['time_start'] + timedelta(hours=reservation[0]['time_select'])
        return {"msg": "This locker had reservation",
                "end_time": f"{end - datetime.now()} left"}

@router.post("/create", status_code=200)
def create_reservation_locker(reservation: Reservation):
    #validation reservation
    if reservation.user_id == "":
        raise HTTPException(status_code=400, detail="User id must not empty")
    if sum([1 for i in reservation.user_id if i.isalpha()]) > 0:
        raise HTTPException(status_code=400, detail="Invalid user id")
    if reservation.locker_id not in range(0,6):
        raise HTTPException(status_code=400, detail="Locker id must be in range 0-5")
    if reservation.backpack == []:
        raise HTTPException(status_code=400, detail="Backpack must not empty")
    if reservation.time_select <= 0:
        raise HTTPException(status_code=400, detail="Time select must be greater than 0")

    #check available locker
    locker = db["locker"].find_one({"locker_id": reservation.locker_id})
    if locker is None or locker["available"] == False:
        raise HTTPException(status_code=400, detail="Locker is not available")
    
    reservation.time_start = datetime.now()
    if reservation.time_select <= 2:
        reservation.fee = 0
    else:
        reservation.fee = (reservation.time_select - 2) * 5
    
    db["reservation_locker"].insert_one(reservation.dict())
    
    reservation = db["reservation_locker"].find_one(reservation.dict())
    
    db["locker"].update_one(
        {
            "locker_id": reservation["locker_id"]
        },
        {
            "$set": {
                "available": False,
                "reservation_id": reservation["_id"],
            }
        }
    )

    return {"msg": "Create Success"}


@router.delete("/{user_id}/{money}")
def delete_reservation_locker(user_id: str, money: float):
    reserve_collection = db['reservation_locker']
    locker_collection = db['locker']
    values = list(reserve_collection.find({"user_id": user_id}, {'_id': False}))

    if len(values) == 0:
        raise HTTPException(status_code=404, detail="Reservation not found")
    elif len(values) > 1:
        raise HTTPException(status_code=500, detail="Something went wrong (len > 1)")
    elif len(values) == 1:
        resp = values[0]
        locker_id = values[0]['locker_id']
        items = values[0]['backpack']

        fee = resp['fee']
        time_user = timedelta(hours=resp['time_select'])
        real_time_used = datetime.now() - resp['time_start']

        time_exceed = real_time_used - time_user
        if (time_exceed <= timedelta(0)):
            resp = reserve_collection.delete_one({"user_id": user_id})
            resp = locker_collection.update_one({'locker_id': locker_id}, {"$set": {"available": True}})

            return {'items': items, 'change_back': money}

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
                resp = locker_collection.update_one({'locker_id': locker_id}, {"$set": {"available": True}})

                change = f"{(money-total_fee):.3f}"
                return {'items': items, 'change_back': change}


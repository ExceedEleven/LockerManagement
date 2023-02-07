from datetime import datetime
from fastapi import Body, APIRouter, HTTPException
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
    pass


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
    reservation.end_time = None
    
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
    pass
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db
from database.schemas.room_schema import (
    RoomCreate,
    RoomUpdate,
    RoomResponse,
)

from backend.services.room_service import RoomService

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
):
    return RoomService.create(db, room)


@router.get(
    "/",
    response_model=list[RoomResponse],
)
def get_rooms(
    db: Session = Depends(get_db),
):
    return RoomService.get_all(db)


@router.get(
    "/{room_id}",
    response_model=RoomResponse,
)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    return RoomService.get(db, room_id)


@router.put(
    "/{room_id}",
    response_model=RoomResponse,
)
def update_room(
    room_id: int,
    room: RoomUpdate,
    db: Session = Depends(get_db),
):
    return RoomService.update(db, room_id, room)


@router.delete(
    "/{room_id}",
)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    RoomService.delete(db, room_id)

    return {
        "message": "Room deleted successfully"
    }
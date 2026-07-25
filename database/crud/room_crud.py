"""
=========================================================
Room CRUD Operations
=========================================================
"""

from sqlalchemy.orm import Session

from database.models import Room
from database.schemas.room_schema import (
    RoomCreate,
    RoomUpdate,
)


def create_room(db: Session, room: RoomCreate) -> Room:
    db_room = Room(**room.model_dump())

    db.add(db_room)

    db.commit()

    db.refresh(db_room)

    return db_room


def get_room(db: Session, room_id: int):

    return db.query(Room).filter(Room.id == room_id).first()


def get_rooms(db: Session):

    return db.query(Room).all()


def update_room(
    db: Session,
    room_id: int,
    room_update: RoomUpdate
):

    room = get_room(db, room_id)

    if room is None:
        return None

    update_data = room_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():

        setattr(room, key, value)

    db.commit()

    db.refresh(room)

    return room


def delete_room(
    db: Session,
    room_id: int
):

    room = get_room(db, room_id)

    if room is None:
        return None

    db.delete(room)

    db.commit()

    return room
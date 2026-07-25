"""
=========================================================
Room Service
=========================================================
"""

from sqlalchemy.orm import Session

from database.crud.room_crud import (
    create_room,
    get_room,
    get_rooms,
    update_room,
    delete_room,
)

from database.schemas.room_schema import (
    RoomCreate,
    RoomUpdate,
)

from backend.utils.exceptions import RoomNotFound


class RoomService:

    @staticmethod
    def create(db: Session, room: RoomCreate):
        return create_room(db, room)

    @staticmethod
    def get(db: Session, room_id: int):
        room = get_room(db, room_id)

        if room is None:
            raise RoomNotFound()

        return room

    @staticmethod
    def get_all(db: Session):
        return get_rooms(db)

    @staticmethod
    def update(db: Session, room_id: int, room_update: RoomUpdate):
        room = update_room(db, room_id, room_update)

        if room is None:
            raise RoomNotFound()

        return room

    @staticmethod
    def delete(db: Session, room_id: int):
        room = delete_room(db, room_id)

        if room is None:
            raise RoomNotFound()

        return room
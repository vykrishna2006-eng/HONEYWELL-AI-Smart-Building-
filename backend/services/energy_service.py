"""
=========================================================
Energy Service
=========================================================
"""

from sqlalchemy.orm import Session

from database.crud.energy_crud import (
    create_energy,
    get_energy,
    get_energies,
    update_energy,
    delete_energy,
)

from database.schemas.energy_schema import (
    EnergyCreate,
    EnergyUpdate,
)

from backend.utils.exceptions import EnergyNotFound


class EnergyService:

    @staticmethod
    def create(
        db: Session,
        energy: EnergyCreate,
    ):
        return create_energy(db, energy)

    @staticmethod
    def get(
        db: Session,
        energy_id: int,
    ):
        energy = get_energy(db, energy_id)

        if energy is None:
            raise EnergyNotFound()

        return energy

    @staticmethod
    def get_all(
        db: Session,
    ):
        return get_energies(db)

    @staticmethod
    def update(
        db: Session,
        energy_id: int,
        energy_update: EnergyUpdate,
    ):
        energy = update_energy(
            db,
            energy_id,
            energy_update,
        )

        if energy is None:
            raise EnergyNotFound()

        return energy

    @staticmethod
    def delete(
        db: Session,
        energy_id: int,
    ):
        energy = delete_energy(
            db,
            energy_id,
        )

        if energy is None:
            raise EnergyNotFound()

        return energy
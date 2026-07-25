"""
=========================================================
Energy CRUD Operations
=========================================================
"""

from sqlalchemy.orm import Session

from database.models import Energy
from database.schemas.energy_schema import (
    EnergyCreate,
    EnergyUpdate,
)


def create_energy(
    db: Session,
    energy: EnergyCreate,
):
    db_energy = Energy(**energy.model_dump())

    db.add(db_energy)
    db.commit()
    db.refresh(db_energy)

    return db_energy


def get_energy(
    db: Session,
    energy_id: int,
):
    return (
        db.query(Energy)
        .filter(Energy.id == energy_id)
        .first()
    )


def get_energies(
    db: Session,
):
    return db.query(Energy).all()


def update_energy(
    db: Session,
    energy_id: int,
    energy_update: EnergyUpdate,
):
    energy = get_energy(db, energy_id)

    if energy is None:
        return None

    update_data = energy_update.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(energy, key, value)

    db.commit()
    db.refresh(energy)

    return energy


def delete_energy(
    db: Session,
    energy_id: int,
):
    energy = get_energy(db, energy_id)

    if energy is None:
        return None

    db.delete(energy)
    db.commit()

    return energy
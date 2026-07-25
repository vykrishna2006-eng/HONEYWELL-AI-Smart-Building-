from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db

from database.schemas.energy_schema import (
    EnergyCreate,
    EnergyUpdate,
    EnergyResponse,
)

from backend.services.energy_service import EnergyService

router = APIRouter(
    prefix="/energy",
    tags=["Energy"],
)


@router.post(
    "/",
    response_model=EnergyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_energy(
    energy: EnergyCreate,
    db: Session = Depends(get_db),
):
    return EnergyService.create(db, energy)


@router.get(
    "/",
    response_model=list[EnergyResponse],
)
def get_energies(
    db: Session = Depends(get_db),
):
    return EnergyService.get_all(db)


@router.get(
    "/{energy_id}",
    response_model=EnergyResponse,
)
def get_energy(
    energy_id: int,
    db: Session = Depends(get_db),
):
    return EnergyService.get(db, energy_id)


@router.put(
    "/{energy_id}",
    response_model=EnergyResponse,
)
def update_energy(
    energy_id: int,
    energy: EnergyUpdate,
    db: Session = Depends(get_db),
):
    return EnergyService.update(
        db,
        energy_id,
        energy,
    )


@router.delete("/{energy_id}")
def delete_energy(
    energy_id: int,
    db: Session = Depends(get_db),
):
    EnergyService.delete(
        db,
        energy_id,
    )

    return {
        "message": "Energy record deleted successfully"
    }
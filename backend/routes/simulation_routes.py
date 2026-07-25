from fastapi import APIRouter
from energyplus.simulator import simulate

router = APIRouter(
    prefix="/simulation",
    tags=["Simulation"],
)

@router.post("/run")
async def run_simulation():
    return simulate()
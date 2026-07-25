from backend.services.simulation_service import SimulationService

service = SimulationService()

def simulation():
    return service.run_simulation()
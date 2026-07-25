from backend.services.simulation_service import SimulationService
from llm.service import LLMService


def run_simulation():
    """
    Run EnergyPlus simulation.
    """
    service = SimulationService()
    return service.run_simulation()


def ai_recommendation():
    """
    Generate AI recommendation.
    """
    return LLMService.recommend()
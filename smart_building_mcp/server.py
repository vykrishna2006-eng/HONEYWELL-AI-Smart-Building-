from fastmcp import FastMCP

from smart_building_mcp.analytics_tool import get_dashboard
from smart_building_mcp.prediction_tool import predict
from smart_building_mcp.simulation_tool import simulation
from smart_building_mcp.recommendation_tool import recommendation

mcp = FastMCP("AI Smart Building MCP")


@mcp.tool
def predict_energy(sensor_data: dict):
    print("Received from MCP:", sensor_data)
    return predict(sensor_data)

@mcp.tool
def predict_energy(sensor_data: dict):
    return predict(sensor_data)


@mcp.tool
def run_simulation():
    return simulation()


@mcp.tool
def ai_recommendation():
    return recommendation()


if __name__ == "__main__":
    mcp.run()
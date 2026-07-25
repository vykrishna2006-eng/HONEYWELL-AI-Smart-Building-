from ml.optimization.constraints import BuildingConstraints


class RuleEngine:

    def generate_rules(self, data):

        recommendations = []

        # HVAC
        if data["predicted_energy_kWh"] > BuildingConstraints.MAX_ENERGY:
            recommendations.append(
                "Reduce HVAC cooling by 1°C."
            )

        # Comfort
        if data["predicted_comfort_score"] < BuildingConstraints.MIN_COMFORT:
            recommendations.append(
                "Increase fresh air circulation."
            )

        # CO₂
        if data["CO2_ppm"] > BuildingConstraints.MAX_CO2:
            recommendations.append(
                "Increase ventilation."
            )

        # Humidity
        if data["Humidity_Percent"] > BuildingConstraints.MAX_HUMIDITY:
            recommendations.append(
                "Enable dehumidification."
            )

        # Occupancy
        if data["Occupancy"] == 0:
            recommendations.append(
                "Turn OFF HVAC and Lighting."
            )

        if not recommendations:
            recommendations.append(
                "System is operating efficiently."
            )

        return recommendations
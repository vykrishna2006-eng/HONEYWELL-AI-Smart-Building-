from ml.optimization.constraints import BuildingConstraints
from ml.optimization.rule_engine import RuleEngine
from ml.optimization.objective import OptimizationObjective


class Optimizer:
    """
    Optimizes building operation based on
    ML predictions and business constraints.
    """

    def __init__(self):
        self.rule_engine = RuleEngine()

    def optimize(
        self,
        sensor_data: dict,
        prediction: dict,
        objective: str = OptimizationObjective.BALANCED
    ) -> dict:
        """
        Optimize the building operation.

        Parameters
        ----------
        sensor_data : dict
            Current sensor values

        prediction : dict
            Output from Predictor

        objective : str
            Optimization objective

        Returns
        -------
        dict
        """

        energy = prediction["predicted_energy_kWh"]
        comfort = prediction["predicted_comfort_score"]

        recommendations = self.rule_engine.generate_rules(
            {
                **sensor_data,
                **prediction
            }
        )

        # ------------------------------------------------
        # Default Recommendation
        # ------------------------------------------------

        recommended_setpoint = sensor_data["HVAC_Setpoint_C"]

        expected_saving = 0.0

        # ------------------------------------------------
        # Energy Optimization
        # ------------------------------------------------

        if objective == OptimizationObjective.MINIMIZE_ENERGY:

            if energy > BuildingConstraints.MAX_ENERGY:

                recommended_setpoint += 1

                expected_saving = 12.0

        # ------------------------------------------------
        # Comfort Optimization
        # ------------------------------------------------

        elif objective == OptimizationObjective.MAXIMIZE_COMFORT:

            if comfort < BuildingConstraints.MIN_COMFORT:

                recommended_setpoint -= 1

                expected_saving = 3.0

        # ------------------------------------------------
        # Balanced Optimization
        # ------------------------------------------------

        else:

            if energy > BuildingConstraints.MAX_ENERGY:

                recommended_setpoint += 1

                expected_saving += 8.0

            if comfort < BuildingConstraints.MIN_COMFORT:

                recommended_setpoint -= 1

        # ------------------------------------------------
        # Respect Building Constraints
        # ------------------------------------------------

        recommended_setpoint = max(
            BuildingConstraints.MIN_HVAC_SETPOINT,
            min(
                BuildingConstraints.MAX_HVAC_SETPOINT,
                recommended_setpoint
            )
        )

        return {

            "objective": objective,

            "predicted_energy_kWh": round(energy, 2),

            "predicted_comfort_score": round(comfort, 2),

            "recommended_hvac_setpoint": recommended_setpoint,

            "expected_energy_saving_percent": round(expected_saving, 2),

            "recommendations": recommendations
        }
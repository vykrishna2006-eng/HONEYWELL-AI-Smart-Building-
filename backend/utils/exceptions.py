"""
=========================================================
Custom Exceptions
=========================================================
"""


class RoomNotFound(Exception):
    def __init__(self, message: str = "Room not found"):
        self.message = message
        super().__init__(self.message)


class SensorNotFound(Exception):
    def __init__(self, message: str = "Sensor not found"):
        self.message = message
        super().__init__(self.message)


class EnergyNotFound(Exception):
    def __init__(self, message: str = "Energy record not found"):
        self.message = message
        super().__init__(self.message)


class PredictionNotFound(Exception):
    def __init__(self, message: str = "Prediction not found"):
        self.message = message
        super().__init__(self.message)


class RecommendationNotFound(Exception):
    def __init__(self, message: str = "Recommendation not found"):
        self.message = message
        super().__init__(self.message)
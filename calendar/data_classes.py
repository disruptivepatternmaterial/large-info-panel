from datetime import datetime

from weather.constants import WeatherCondition


class Weather:
    def __init__(self, temperature: float, condition: str, sunrise: float, sunposition: float):
        self.temperature = temperature
        try:
            self.condition = WeatherCondition(condition)
        except ValueError:
            self.condition = WeatherCondition.SNOW
        self.sunrise = datetime.fromtimestamp(sunrise)
        self.sunposition = datetime.fromtimestamp(sunposition)


class WeatherData:
    def __init__(self, current: Weather):
        self.current = current

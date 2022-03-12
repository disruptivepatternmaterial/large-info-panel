from weather.constants import WeatherCondition


class Weather:
    def __init__(self, temperature: int, condition: str, sunrise: int):
        self.temperature = temperature
        try:
            self.condition = WeatherCondition(condition)
        except ValueError:
            self.condition = WeatherCondition.CLOUDS
        self.sunrise = sunrise


class WeatherData:
    def __init__(self, current: Weather):
        self.current = current

from weather.open_weather import OpenWeatherDataThread


class Data:
    _data = {
        "weather": OpenWeatherDataThread(refresh_rate=30, daemon=True),
    }

    @classmethod
    def get(cls, key: str) -> object:
        return cls._data[key].data

    @classmethod
    def start_all_data_threads(cls):
        for thread in cls._data.values():
            thread.start()

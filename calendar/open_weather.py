import time
from typing import Dict

from config import Config
from common.api_client import APIClient, RequestMethod
from common.threading import DataThread
from weather.data_classes import Weather, WeatherData


class OpenWeatherAPIClient(APIClient):
    api_key_param = "appid"

    @classmethod
    def _get_base_url(seclslf, *args, **kwargs) -> str:
        #return "https://api.openweathermap.org/data/2.5/"
        return "http://192.168.50.10:1880/"

    @classmethod
    def _get_api_key(cls, *args, **kwargs) -> str:
        return
        #return Config.get()["weather"]["api_key"]

    @classmethod
    def get_current_weather(cls, location: str = None) -> Weather:
        config = Config.get()
        if not location:
            location = config["weather"]["location"]
        response = cls._make_request(
            method=RequestMethod.GET,
            path="rgbpanel/environment/",
            #path="weather",
            #params=dict(q=location, units=config["weather"]["units"]),
        )
        temperature=float(response[5]["_value"])
        condition="SNOW"

        response2 = cls._make_request(
            method=RequestMethod.GET,
            path="sundata/",
        )
        #imes.sunrise.ts
        sunrise=round(response2["times"]["sunrise"]["ts"] / 1000, 0)
        sunposition=round(response2["altitudePercent"], 2)

        #print(temperature)
        #print(condition)
        #print(sunrise)
        #print(sunposition)

        #print(response)

        return Weather(
            temperature,
            #temperature=int(response["main"]["temp"]),
            condition,
            sunrise,
            sunposition,
            #condition=response["weather"][0]["main"],
            #sunrise=1664566938,
            #sunrise=response["sys"]["sunrise"],
        )



class OpenWeatherDataThread(DataThread):
    def _fetch_data(self) -> WeatherData:
        try:
            current_weather = OpenWeatherAPIClient.get_current_weather()
            print(current_weather)
        # If call fails, just return existing data
        except:
            return self._data
        return WeatherData(current=current_weather)

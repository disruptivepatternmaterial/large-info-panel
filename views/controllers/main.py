from datetime import datetime, timedelta

from rgbmatrix import RGBMatrix

from common.threading import RestartableThread
from config import Config
from data import Data
from views.clock import ClockView
from views.controllers.base_controllers import BaseController
from views.controllers.looping_threads import LoopingThreadsController
from views.night_time import NightTimeView
from views.sunrise import SunriseView
from views.weather import WeatherView


class MainController(BaseController):
    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._clock_and_weather_controller = RestartableThread(
            thread=LoopingThreadsController,
            threads=[
                {
                    "key": "clock",
                    "instance": RestartableThread(
                        thread=ClockView,
                        rgb_matrix=self._rgb_matrix,
                    ),
                },
                {
                    "key": "weather",
                    "instance": RestartableThread(
                        thread=WeatherView,
                        rgb_matrix=self._rgb_matrix,
                    ),
                },
            ],
            thread_change_delay=10,
        )
        self._night_time_controller = RestartableThread(
            thread=NightTimeView,
            rgb_matrix=self._rgb_matrix,
        )
        self._sunrise_controller = RestartableThread(
            thread=SunriseView,
            rgb_matrix=self._rgb_matrix,
        )
        self._set_current_thread(thread=self._clock_and_weather_controller)

    def _update_thread(self):
        weather_data = Data.get("weather")
        if not weather_data:
            return

        current_time = datetime.now()
        sunrise_start = weather_data.current.sunrise
        sunrise_end = sunrise_start + timedelta(minutes=Config.get()["sunrise"]["duration"])
        # Switch to the sunrise view
        if sunrise_start <= current_time <= sunrise_end:
            # Only switch views if we aren't showing it already
            if self._current_thread != self._sunrise_controller:
                self._switch_thread(thread=self._sunrise_controller)
        # Switch to the night time view
        elif current_time.hour >= Config.get()["night_time"]["start_time"] or current_time.hour < sunrise_start:
            # Only switch views if we aren't showing it already
            if self._current_thread != self._night_time_controller:
                self._switch_thread(thread=self._night_time_controller)
        # Switch to the clock and weather view
        else:
            # Only switch views if we aren't showing it already
            if self._current_thread != self._clock_and_weather_controller:
                self._switch_thread(thread=self._clock_and_weather_controller)
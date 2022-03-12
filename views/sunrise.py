from datetime import datetime, timedelta

from config import Config
from data import Data
from graphics.color import Color
from graphics.shapes import draw_rectangle
from views.base_views import BaseView
from weather.constants import WeatherCondition


class SunriseView(BaseView):
    _render_delay = 1

    def _render(self):
        # Get weather data
        weather_data = Data.get("weather")
        if not weather_data:
            return
        # Get duration
        duration = Config.get()["sunrise"]["duration"]
        # Calculate position, size, etc.
        start_time = weather_data.current.sunrise
        end_time = start_time + timedelta(minutes=duration)
        #current_time = datetime.now()
        current_time = start_time + timedelta(minutes=20)
        progress = (end_time-current_time).seconds / (end_time-start_time).seconds
        print(progress)
        height = int(self._rgb_matrix.height * (1-progress))
        print(self._rgb_matrix.height)
        print(height)
        # Render sunrise
        draw_rectangle(
            canvas=self._offscreen_canvas,
            x_pos=0,
            y_pos=self._rgb_matrix.height-height,
            height=height,
            width=self._rgb_matrix.width,
            color=Color.YELLOW.value,
        )

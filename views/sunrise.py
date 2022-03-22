import math
from datetime import datetime, timedelta

from rgbmatrix import graphics

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
        # Calculate position, size, color, etc.
        start_time = weather_data.current.sunrise
        end_time = start_time + timedelta(minutes=duration)
        current_time = datetime.now()
        progress = (1-(end_time-current_time).seconds / (end_time-start_time).seconds)
        # Clamp progress between 0 and 1
        progress = max(min(progress, 1), 0)
        height = math.ceil(self._rgb_matrix.height * progress)
        color = graphics.Color(
            Color.ORANGE.value.red * progress,
            Color.ORANGE.value.green * progress,
            Color.ORANGE.value.blue * progress,
        )
        # Render sunrise
        draw_rectangle(
            canvas=self._offscreen_canvas,
            x_pos=0,
            y_pos=self._rgb_matrix.height-height,
            height=height,
            width=self._rgb_matrix.width,
            color=color,
        )

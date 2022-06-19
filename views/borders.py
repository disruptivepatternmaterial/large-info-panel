from PIL import Image
from typing import Dict
import json

from rgbmatrix import graphics, RGBMatrix

from config import Config
from data import Data
from graphics.font import Font, FontStyle
from graphics.utils import center_object
from graphics.utils import center_text
from utils import get_abs_file_path
from views.base_views import BaseView
from weather.constants import WeatherCondition

CELCIUS_INDICATOR_WIDTH = 3
CONDITION_ICON_WIDTH = 15
MARGIN_WIDTH = 3
WEATHER_CONDITION_ICON_MAP = {
    WeatherCondition.CLEAR: dict(name="sunny", x_offset=-1, y_offset=1),
    WeatherCondition.CLOUDS: dict(name="cloudy", y_offset=1),
    WeatherCondition.RAIN: dict(name="rainy", x_offset=-1),
    WeatherCondition.DRIZZLE: dict(name="rainy", x_offset=-1),
    WeatherCondition.THUNDERSTORM: dict(name="stormy", x_offset=-1),
    WeatherCondition.SNOW: dict(name="snowy", x_offset=-1),
}

class BorderView(BaseView):
    _render_delay = 5

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        self._font, self._font_size = Font.get_font(FontStyle.SMALL)
        self._col1 = 0
        self._col2 = 70
        self._col3 = 120
        self._col4 = 170
        self._col5 = 220

    def _render_colums_headers(self):
        color = graphics.Color(*Config.get()["weather"]["temperature_color"])
        
        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            self._col1 + 1,
            20,
            color,
            "room",
        )
        pass
        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            self._col2 + 1,
            20,
            color,
            "°F",
        )
        pass

        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            self._col3 + 1,
            20,
            color,
            "RH%",
        )
        pass

        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            self._col4 + 1,
            20,
            color,
            "pm25",
        )
        pass

        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            self._col5 + 1,
            20,
            color,
            "CO2",
        )
        pass

    def _render_temperature(self, data: json, x_pos: int, y_pos: int):

        for i in range(len(data)):
            try:
                pm25 = str(round(float(data[i]["pm25"]),1)) + ""
            except:
                pm25 = ""
            
            try:
                co2 = str(round(data[i]["co2"])) + ""
            except:
                co2 = ""

            if data[i]["room"] == 'livingroom':
                data[i]["room"] = 'living'
            
            color = graphics.Color(*Config.get()["weather"]["temperature_color"])

            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                self._col1,
                y_pos + self._font_size["height"],
                color,
                data[i]["room"] + ":",
            )

            #temperature
            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                self._col2,
                y_pos + self._font_size["height"],
                graphics.Color(int(data[i]["temp-color"][0]),int(data[i]["temp-color"][1]),int(data[i]["temp-color"][2])),
                str(round(data[i]["temperature_F"],1)) + "",
            )

            #humidity    
            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                self._col3,
                y_pos + self._font_size["height"],
                graphics.Color(int(data[i]["humidity-color"][0]),int(data[i]["humidity-color"][1]),int(data[i]["humidity-color"][2])),
                str(round(float(data[i]["humidity"]),1)) + "",
            )
            #pm25
            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                self._col4,
                y_pos + self._font_size["height"],
                graphics.Color(int(data[i]["pm25-color"][0]),int(data[i]["pm25-color"][1]),int(data[i]["pm25-color"][2])),
                pm25,
            )
            
            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                self._col5,
                y_pos + self._font_size["height"],
                graphics.Color(int(data[i]["co2-color"][0]),int(data[i]["co2-color"][1]),int(data[i]["co2-color"][2])),
                co2,
            )
            #this moves us down
            y_pos = y_pos + 25

        #graphics.DrawCircle(
        #    self._offscreen_canvas,
        #    x_pos + len(temperature) * self._font_size["width"] + 1,
        #    y_pos,
        #    1,
        #    color,
        #)

    def _render_condition_icon(self, icon_name: str, x_pos: int, y_pos: int):
        if icon_name != self._icon_name:
            self._icon = Image.open(
                get_abs_file_path(f"assets/{icon_name}.png")
            ).convert("RGB")
            self._icon_name = icon_name
            #print(self._icon_name)
        self._icon.resize(
            (self._rgb_matrix.width, self._rgb_matrix.height), Image.ANTIALIAS
        )
        self._offscreen_canvas.SetImage(self._icon, x_pos, y_pos, unsafe=False)

    def _render(self):
        # Get weather data
        self._rgb_matrix.brightness = 80
        weather_data = Data.get("weather")

        if weather_data:
            data = weather_data.current.inside_data
            sunrise =  weather_data.current.sunrise
            sunposition =  weather_data.current.sunposition
        
        x_pos = 0
        y_pos = 25
        margin_width = 1

        self._render_colums_headers()

        self._render_temperature(
            data = data,
            x_pos=x_pos + margin_width,
            y_pos=y_pos + margin_width,
        )
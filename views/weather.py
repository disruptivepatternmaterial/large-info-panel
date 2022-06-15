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


class WeatherView(BaseView):
    _render_delay = 5

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        self._font, self._font_size = Font.get_font(FontStyle.SMALL)
        self._co2_font, self._co2_font_size = Font.get_font(FontStyle.LARGE)

    def _render_temperature(self, data: json, x_pos: int, y_pos: int):
        color = graphics.Color(*Config.get()["weather"]["temperature_color"])
        color_green = graphics.Color(10, 200, 10)
        color_yellow = graphics.Color(200, 200, 10)
        color_red = graphics.Color(200, 10, 10)
        color_blue = graphics.Color(10, 10, 200)
        co2 = 0
        for i in range(len(data)):
            try:
                pm25 = str(round(data[i]["pm25"],1)) + " pm25"
                if round(data[i]["pm25"],1) >= 10:
                    pm25_color = color_red
                elif round(data[i]["pm25"],1) <=2:
                    pm25_color = color_green
                else:
                    pm25_color = color_yellow
            except:
                pm25 = ""
            try:
                co2 = "  CO2: " + str(round(data[i]["co2"])) + " ppm"
                if round(data[i]["co2"]) >= 1300:
                    co2_color = color_red
                elif round(data[i]["co2"]) <=500:
                    co2_color = color_green
                else:
                    co2_color = color_yellow
            except:
                pass

            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                x_pos,
                y_pos + self._font_size["height"],
                color,
                data[i]["room"] + ":",
            )

            if round(data[i]["temperature_F"]) >= 85:
                temp_color = color_red
            elif round(data[i]["temperature_F"]) <=60:
                temp_color = color_blue
            else:
                temp_color = color_green

            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                x_pos+85,
                y_pos + self._font_size["height"],
                temp_color,
                str(round(data[i]["temperature_F"])) + "°F",
            )


            if round(data[i]["humidity"]) >= 60:
                rh_color = color_red
            elif round(data[i]["humidity"]) <= 20:
                rh_color = color_blue
            else:
                rh_color = color_green
                
            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                x_pos+130,
                y_pos + self._font_size["height"],
                rh_color,
                str(round(data[i]["humidity"])) + "%",
            )

            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                x_pos+170,
                y_pos + self._font_size["height"],
                pm25_color,
                pm25,
            )

            y_pos = y_pos + 25

        x_pos = center_text(center_pos=140, text=co2, font_width=self._co2_font_size["width"])

        graphics.DrawText(
            self._offscreen_canvas,
            self._co2_font,
            x_pos,
            y_pos + self._font_size["height"] + 15,
            co2_color,
            co2,
        )



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
        #print(data)
        temperature = data[3]["temperature_F"]
        x_pos = 2
        y_pos = 2
        margin_width = 1
        self._render_temperature(
            data = data,
            #temperature=str(temperature),
            x_pos=x_pos + margin_width,
            y_pos=x_pos + margin_width,
        )
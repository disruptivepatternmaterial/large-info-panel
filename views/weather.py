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
from graphics.shapes import draw_rectangle

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
        self._col1 = 2   #room
        self._col2 = 75  #temp
        self._col3 = 102 #rh
        self._col4 = 130 #AQI
        self._col5 = 170 #co2
        self._col6 = 210 #VOC

    def _render_colums_headers(self):
        color = graphics.Color(*Config.get()["weather"]["temperature_color"])
        background = graphics.Color(50,50,50)
        black = graphics.Color(0,0,0)
        draw_rectangle(
            canvas=self._offscreen_canvas,
            x_pos=0,
            y_pos=0,
            height=self._rgb_matrix.width,
            width=self._rgb_matrix.width,
            color=background,
        )
        draw_rectangle(
            canvas=self._offscreen_canvas,
            x_pos=70,
            y_pos=25,
            height=self._rgb_matrix.height-2,
            width=self._rgb_matrix.width-2,
            color=black,
        )          

        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            self._col1 + 1,
            20,
            color,
            "",
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
            "RH",
        )
        pass

        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            self._col4 + 1,
            20,
            color,
            "AQI",
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

        graphics.DrawText(
            self._offscreen_canvas,
            self._font,
            self._col6 + 1,
            20,
            color,
            "VOC",
        )
        pass   

    def _render_temperature(self, data: json, x_pos: int, y_pos: int):

        for i in range(len(data)):
            try:
                pm25 = str(round(float(data[i]["PM25"]))) + ""
            except:
                pm25 = ""
            
            try:
                co2 = str(round(data[i]["CO2"])) + ""
            except:
                co2 = ""

            try:
                voc = str(round(data[i]["VOC"])) + ""
            except:
                voc = ""

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
                str(round(data[i]["Temperature_F"])) + "",
            )

            #humidity    
            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                self._col3,
                y_pos + self._font_size["height"],
                graphics.Color(int(data[i]["humidity-color"][0]),int(data[i]["humidity-color"][1]),int(data[i]["humidity-color"][2])),
                str(round(float(data[i]["Humidity"]))) + "",
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

            graphics.DrawText(
                self._offscreen_canvas,
                self._font,
                self._col6,
                y_pos + self._font_size["height"],
                graphics.Color(int(data[i]["voc-color"][0]),int(data[i]["voc-color"][1]),int(data[i]["voc-color"][2])),
                voc,
            )            
            #this moves us down
            y_pos = y_pos + 20

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
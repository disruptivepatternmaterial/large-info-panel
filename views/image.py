from PIL import Image
from typing import Dict

from rgbmatrix import graphics, RGBMatrix

from config import Config
from data import Data
from graphics.font import Font, FontStyle
from graphics.utils import center_object
from utils import get_abs_file_path
from views.base_views import BaseView
from weather.constants import WeatherCondition
from animations.pulsing_text import PulsingTextAnimation
from animations.scrolling_text import ScrollingTextAnimation
import random
import os
import requests
from io import BytesIO

class ImageView(BaseView):
    _render_delay = Config.get()["timing"]["imageswap"]

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        self._icon = None
        self._icon_name = None
        self._font, self._font_size = Font.get_font(FontStyle.LARGE)

    def _render_temperature(self):
        color = graphics.Color(*Config.get()["weather"]["temperature_color"])
        ScrollingTextAnimation(
            text="this is a test of the scrolling of text",
            font= self._font,
            font_size = self._font_size,
            color=color,
            starting_x_pos=100,
            starting_y_pos=100,
            speed=5,
            max_cycles=None,
            wait_until_armed = False,
        )

    def _render_condition_icon(self):
        #get_abs_file_path(f"assets/island-summer-Meredith-Moench.png")
        self._icon = Image.open("/home/ntableman/sunrise-alarm-clock/artwork/" + 
                random.choice(os.listdir("/home/ntableman/sunrise-alarm-clock/artwork"))
            ).convert("RGB").resize((256, 192), Image.ANTIALIAS)
        #curl -H "Authorization: Bearer eyJrIjoiQlF6cExqS3pxVWZxZjJqTm1FaTFqOGRoNFVZRUNzU1oiLCJuIjoidGVzdGluZy1wYW5lbC1ncmFiYmVyIiwiaWQiOjF9" http://lf-hub:3000/api/dashboards/home
        #auth_token='eyJrIjoiQlF6cExqS3pxVWZxZjJqTm1FaTFqOGRoNFVZRUNzU1oiLCJuIjoidGVzdGluZy1wYW5lbC1ncmFiYmVyIiwiaWQiOjF9'
        #head = {'Authorization': 'Bearer ' + auth_token}
        #url = "http://lf-hub:3000/render/d/9yd-Cgj7z/small-border-wait-times?width=768&height=576&frameborder=0&kiosk"
        #response = requests.get(url=url, headers=head, stream=True, timeout=5000)
        #self._icon = Image.open(BytesIO(response.content)).convert('RGB').resize((256, 192), Image.ADAPTIVE)
        #self._icon.resize(
        #    (256, 192)
        #)
        self._offscreen_canvas.SetImage(self._icon, 0, 0, unsafe=True)

    def _render(self):
        # Get weather data

        # Render condition icon and temperature
        self._render_condition_icon()
        self._render_temperature()
        #self._outline_canvas_animation.render(canvas=self._offscreen_canvas)

   #http://lf-hub:3000/d/9yd-Cgj7z/small-border-wait-times?orgId=1&refresh=1m
   #http://lf-hub:3000/render/d/9yd-Cgj7z/small-border-wait-times?width=512&height=384&frameborder=0&kiosk
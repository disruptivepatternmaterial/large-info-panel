from datetime import datetime

from rgbmatrix import graphics, RGBMatrix

from animations.outline_canvas import OutlineCanvasAnimation
from config import Config
from graphics.font import Font, FontStyle
from graphics.utils import center_text
from views.base_views import BaseView
from PIL import Image
import random
import os
import requests
import time


class ClockView(BaseView):
    _render_delay = 0.05

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        self._icon = None
        self._last_minute = None
        self._outline_canvas_animation = OutlineCanvasAnimation(
            max_cycles=None, wait_until_armed=False
        )

    def _render_location(self):
        color = graphics.Color(*Config.get()["clock"]["location_color"])
        font, font_size = Font.get_font(FontStyle.MEDIUM)
        text = "Bellingham, Washington"
        x_pos = center_text(center_pos=128, text=text, font_width=font_size["width"])
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            21,
            color,
            text,
        )

    def _render_holiday(self):
        color = graphics.Color(*Config.get()["clock"]["location_color"])
        font, font_size = Font.get_font(FontStyle.MEDIUM)
        text = "Bellingham, Washington"
        x_pos = center_text(center_pos=128, text=text, font_width=font_size["width"])
        if datetime.now().minute == 2:
            url = "https://holidays.abstractapi.com/v1/?api_key=&country=US&year=" + datetime.now().strftime("%Y") + "&month=12&day="
            response = requests.get(url)
            print(response)
            fish = response.json()
            print(fish)
        else:
            fish = []
        if fish:
            text = fish[0]["name"]
        else:
            text = "empty"
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            50,
            color,
            text,
        )    
        #self._icon = Image.open("/home/ntableman/sunrise-alarm-clock/assets/bellinghamflag-30.png")
        #self._icon.resize(
        #    (30,18), Image.ANTIALIAS
        #)
        #self._offscreen_canvas.SetImage(self._icon.convert("RGB"), 5, 30, unsafe=False)
        #self._offscreen_canvas.SetImage(self._icon.convert("RGB"), 55, 30, unsafe=False)
        #self._offscreen_canvas.SetImage(self._icon.convert("RGB"), 105, 30, unsafe=False)
        #self._offscreen_canvas.SetImage(self._icon.convert("RGB"), 155, 30, unsafe=False)
        #self._offscreen_canvas.SetImage(self._icon.convert("RGB"), 205, 30, unsafe=False)

    def _render_time(self):
        color = graphics.Color(*Config.get()["clock"]["time_color"])
        font, font_size = Font.get_font(FontStyle.HUGE)
        time = datetime.now().strftime("%A")
        x_pos = center_text(center_pos=128, text=time, font_width=font_size["width"])
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            148,
            color,
            time,
        )

        time = datetime.now().strftime("%B %d")
        x_pos = center_text(center_pos=128, text=time, font_width=font_size["width"])
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            186,
            color,
            time,
        )

        #clock
        time = datetime.now().strftime("%X") #%X
        font, font_size = Font.get_font(FontStyle.MASSIVE)
        x_pos = center_text(center_pos=128, text=time, font_width=font_size["width"])
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            100,
            color,
            time,
        )

    def _render(self):
        # Get current date and time
        now = datetime.now()

        # Reset and arm outline animation every minute
        current_minute = now.minute
        if self._last_minute and self._last_minute != current_minute:
            self._outline_canvas_animation.reset_and_arm()
        self._last_minute = current_minute

        # Render location and time
        self._render_location()
        self._render_time()
        #self._render_holiday()

        # Render outline animation
        self._outline_canvas_animation.render(canvas=self._offscreen_canvas)


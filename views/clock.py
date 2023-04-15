from ctypes.wintypes import RGB
from datetime import datetime

from rgbmatrix import graphics, RGBMatrix

from animations.outline_canvas import OutlineCanvasAnimation
from config import Config
from graphics.font import Font, FontStyle
from graphics.utils import center_text
from views.base_views import BaseView
from PIL import Image, ImageFilter, ImageFont
import random
import os
import requests
import time
import re


class ClockView(BaseView):
    _render_delay = 0.01

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        self._background = None
        self._last_minute = None
        self._background_counter = 0
        self._outline_canvas_animation = OutlineCanvasAnimation(
            max_cycles=None, wait_until_armed=False
        )
    
    def _render_background(self):
        if self._background_counter == 0:
            if datetime.now().month == 6:
                self._background = Image.open("/home/ntableman/large-info-panel/assets/BHam-Flag-Pride.png").convert("RGB").resize((254,190), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(2))
            else:
                self._background = Image.open("/home/ntableman/large-info-panel/assets/bellinghamflag-780x466.png").convert("RGB").resize((254,190), Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(2))
            self._background_counter = 1
        self._offscreen_canvas.SetImage(self._background, 1, 1, unsafe=False)
 
    def _render_location(self):
        color = graphics.Color(*Config.get()["clock"]["location_color"])
        font, font_size = Font.get_font(FontStyle.LARGE) 
        text = "bäärgsiitsch"
        x_pos = center_text(center_pos=127, text=text, font_width=font_size["width"])
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            25,
            color,
            text,
        )

    def _render_holiday(self):
        color = graphics.Color(*Config.get()["clock"]["location_color"])
        font, font_size = Font.get_font(FontStyle.MEDIUM)
        text = "Bellingham, Washington"
        x_pos = center_text(center_pos=127, text=text, font_width=font_size["width"])
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

    def _render_time(self):
        color = graphics.Color(*Config.get()["clock"]["time_color"])
        font, font_size = Font.get_font(FontStyle.XL)
        time = datetime.now().strftime("%A")
        x_pos = center_text(center_pos=127, text=time, font_width=font_size["width"])
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            145,
            color,
            time,
        )

        this_month = datetime.now().strftime("%B")
        n = datetime.now().day
        suffixes = { 1: "st", 2: "nd", 3: "rd" }
        i = n if (n < 20) else (n % 10)
        suffix = suffixes.get(i, 'th')
        time = str(this_month) + "•" + str(n) + suffix
        x_pos = center_text(center_pos=127, text=time, font_width=font_size["width"])
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            183,
            color,
            time,
        )

        #clock
        time = datetime.now().strftime("%X") #%X
        font, font_size = Font.get_font(FontStyle.HUGE)
        x_pos = center_text(center_pos=127, text=time, font_width=font_size["width"])
        graphics.DrawText(
            self._offscreen_canvas,
            font,
            x_pos,
            96,
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
            self._background_counter = 0
            #print("reset and arm")
        self._last_minute = current_minute

        # Render location and time
        self._render_background()
        self._render_location()
        self._render_time()
        # self._render_holiday()

        # Render outline animation
        self._outline_canvas_animation.render(canvas=self._offscreen_canvas)


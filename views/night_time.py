from datetime import datetime

from rgbmatrix import graphics, RGBMatrix

from animations.pulsing_text import PulsingTextAnimation
from config import Config
from graphics.color import Color
from graphics.font import Font, FontStyle
from graphics.gradient import Gradient
from graphics.utils import center_text
from views.base_views import BaseView
import random

BRIGHTNESS_PERCENTAGES = [
    i / 100
    for i in range(0, 100)
][:20]


class NightTimeView(BaseView):
    _render_delay = 0.1

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        text = "sleepytimes " + datetime.now().strftime("%X")
        font, font_size = Font.get_font(FontStyle.SMALL)
        color = graphics.Color(*Config.get()["night_time"]["text_color"])
        x_pos = center_text(center_pos=128, text=text, font_width=font_size["width"])
        y_pos = 100
        self._pulsing_text_animation = PulsingTextAnimation(
            text=text,
            font=font,
            x_pos=x_pos,
            y_pos=y_pos,
            gradient=Gradient.generate_brightness_gradient(
                color=color,
                percentages=BRIGHTNESS_PERCENTAGES + BRIGHTNESS_PERCENTAGES[::-1],
            ),
        )

    def _render(self):
        self._pulsing_text_animation.render(canvas=self._offscreen_canvas)
        self._pulsing_text_animation._text = "sleepytimes " + datetime.now().strftime("%X")
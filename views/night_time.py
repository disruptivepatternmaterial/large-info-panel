from datetime import datetime

from rgbmatrix import graphics, RGBMatrix

from animations.pulsing_text import PulsingTextAnimation
from config import Config
from graphics.color import Color
from graphics.font import Font, FontStyle
from graphics.gradient import Gradient
from graphics.utils import center_text
from views.base_views import BaseView

BRIGHTNESS_PERCENTAGES = [
    i / 100
    for i in range(0, 100)
][:80]


class NightTimeView(BaseView):
    _render_delay = 0.2

    def __init__(self, rgb_matrix: RGBMatrix):
        super().__init__(rgb_matrix)
        text = "Zzz.."
        font, font_size = Font.get_font(FontStyle.LARGE)
        color = Color.YELLOW.value
        x_pos = center_text(center_pos=18, text=text, font_width=font_size["width"])
        self._pulsing_text_animation = PulsingTextAnimation(
            text=text,
            font=font,
            x_pos=x_pos,
            y_pos=15,
            gradient=Gradient.generate_brightness_gradient(
                color=color,
                percentages=[*BRIGHTNESS_PERCENTAGES, *BRIGHTNESS_PERCENTAGES[::-1]],
            ),
        )

    def _render(self):
        self._pulsing_text_animation.render(canvas=self._offscreen_canvas)
from rgbmatrix import RGBMatrix

from views.controllers.base_controllers import BaseController
from views.sunrise import SunriseView


class MainController(BaseController):
    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._set_current_thread(thread=SunriseView(rgb_matrix=self._rgb_matrix))

    def _update_thread(self):
        pass
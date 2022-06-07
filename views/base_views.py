import time
from abc import ABC, abstractmethod

from rgbmatrix import RGBMatrix

from common.threading import StoppableThread


class BaseView(StoppableThread, ABC):
    _render_delay = .005

    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._offscreen_canvas = self._rgb_matrix.CreateFrameCanvas()

    @abstractmethod
    def _render(self):
        pass

    def run(self):
        self._rgb_matrix.brightness = 5
        while True:
            self._offscreen_canvas.Clear()
            self._render()
            self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(
                self._offscreen_canvas
            )
            time.sleep(self._render_delay)
            if self._rgb_matrix.brightness < 100:
                self._rgb_matrix.brightness = self._rgb_matrix.brightness + 5
            if self.stopped:
                break
    
        

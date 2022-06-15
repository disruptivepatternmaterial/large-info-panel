import time
from abc import ABC, abstractmethod

from rgbmatrix import RGBMatrix

from common.threading import StoppableThread

class BaseView(StoppableThread, ABC):
    _render_delay = .05
    _render_type = ""
    _stop_rendering = 0

    def __init__(self, rgb_matrix: RGBMatrix, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rgb_matrix = rgb_matrix
        self._offscreen_canvas = self._rgb_matrix.CreateFrameCanvas()

    @abstractmethod
    def _render(self):
        pass

    def run(self):
        
        print("run entered")
        while True:
            if self._render_type == "image" and self._stop_rendering == 0:
                self._offscreen_canvas.Clear()
                self._render()
                time.sleep(.2)
                self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(
                    self._offscreen_canvas
                )
                for x in range(0, 90, 5):
                    self._rgb_matrix.brightness = x
                    self._offscreen_canvas.SetImage(self._icon, 0, 0, unsafe=True)
                    #self._offscreen_canvas.Clear()
                    self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(
                        self._offscreen_canvas
                    )
                    print(x)
                    time.sleep(.01)
                #time.sleep(self._render_delay)
                self._stop_rendering = 1
                print("image loop done")
            elif self._render_type != "image":
                self._offscreen_canvas.Clear()
                self._render()
                self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(
                    self._offscreen_canvas
                )
                time.sleep(self._render_delay)

                if self._rgb_matrix.brightness < 80:
                    self._rgb_matrix.brightness = self._rgb_matrix.brightness + 5
                    print(self._rgb_matrix.brightness)

            if self.stopped:
                if self._render_type == "image":
                    for x in range(90, 0, -5):
                        time.sleep(.01)
                        self._rgb_matrix.brightness = x
                        self._offscreen_canvas.SetImage(self._icon, 0, 0, unsafe=True)
                    #self._offscreen_canvas.Clear()
                        self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(
                            self._offscreen_canvas
                        )

                else:
                    for x in range(80, 0, -5):
                        time.sleep(.05)
                        self._offscreen_canvas.Clear()
                        self._render()
                        self._offscreen_canvas = self._rgb_matrix.SwapOnVSync(
                            self._offscreen_canvas
                        )
                        self._rgb_matrix.brightness = x
                        print('meow')

                break
    
#ok so since this class is the base for all the render it excutes this run(self), image works because it makes the loop stop with longer _render_delay
#somehow I need to make this loop sensative to the type of trunning
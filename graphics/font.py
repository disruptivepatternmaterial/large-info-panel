import os
from typing import Dict, Optional, Tuple

from enum import Enum

from rgbmatrix import graphics

from utils import get_abs_file_path


class FontStyle(Enum):
    #TINY = "tom-thumb"
    #SMALL = "6x9"
    #MEDIUM = "9x15"
    #LARGE = "10x20"
    TINY = "plex-12"
    SMALL = "plex-18"
    MEDIUM = "plex-24"
    LARGE = "plex-30"
    HUGE = "plex-40"
    MASSIVE = "plex-60"
    ITALIC = "plex-ital-40"

class Font:
    _font_cache = {}

    @classmethod
    def get_font(cls, font_style: FontStyle) -> Tuple[graphics.Font, Optional[Dict]]:
        font_name = font_style.value
        if font_name in cls._font_cache:
            return cls._font_cache[font_name]

        font_paths = ["rpi-rgb-led-matrix/fonts"]
        for font_path in font_paths:
            path = get_abs_file_path(f"{font_path}/{font_name}.bdf")
            if os.path.isfile(path):
                font = graphics.Font()
                font.LoadFont(path)
                size = None
                if font_name.startswith("plex-12"):
                    #TINY
                    size = dict(width=5, height=12)
                elif font_name.startswith("plex-18"):
                    #SMALL
                    size = dict(width=8, height=18)
                elif font_name.startswith("plex-24"):
                    #MEDIUM
                    size = dict(width=13.8, height=24)
                elif font_name.startswith("plex-30"):
                    #LARGE
                    size = dict(width=19, height=30)
                elif font_name.startswith("plex-40"):
                    #HUGE
                    size = dict(width=21, height=40)
                elif font_name.startswith("plex-ital-40"):
                    #ITALIC
                    size = dict(width=28, height=40)
                else:
                    #MASSIVE
                    size = dict(width=28, height=40)   
                #if font_name.startswith("tom"):
                #    size = dict(width=4, height=6)
                #else:
                #    dimensions = font_name.split("x", 1)
                #    if len(dimensions) == 2:
                #        size = dict(width=int(dimensions[0]), height=int(dimensions[1]))
                
                ret = (font, size)
                cls._font_cache[font_name] = ret
                return ret

        raise ValueError(f"Could not find a font for {font_name}!")

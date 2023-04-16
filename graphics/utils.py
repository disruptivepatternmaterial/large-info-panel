from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def center_text(center_pos: int, text: str, font_width: int) -> int:
    return abs(center_pos - ((len(text) * font_width) / 2))

def center_text_new(center_pos: int, text: str, font=None) -> int:
    pixels = textsize(text, font)
    return abs(center_pos - (pixels / 2))

def center_object(center_pos: int, obj_length: int) -> int:
    return abs(center_pos - (obj_length / 2))

def textsize(self, text, font=None, *args, **kwargs):
    """Get the size of a given string, in pixels."""
    #if self._multiline_check(text):
    #    return self.multiline_textsize(text, font, *args, **kwargs)
    # ttf = ImageFont.load  .truetype(font_path, font_size)
    if font is None:
        font = self.getfont()
    return font.getsize(text)

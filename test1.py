from wand.image import Image
from wand.drawing import Drawing
from wand.image import Font
from wand.color import Color
import random

def random_colour_text():
    colours = ['red', 'Maroon', 'Yellow', 'Olive', 'Lime', 'Green', 'Aqua', 'Teal', 'Purple']
    return(random.choice(colours))

def random_font_path_text():
    fonts = ['LiberationMono-BoldItalic.ttf', 'LiberationSansNarrow-Bold.ttf', 
             'LiberationMono-Bold.ttf', 'LiberationSansNarrow-Italic.ttf',
             'LiberationMono-Italic.ttf', 'LiberationSansNarrow-Regular.ttf',
             'LiberationMono-Regular.ttf ', 'LiberationSans-Regular.ttf',
             'LiberationSans-BoldItalic.ttf', 'LiberationSerif-BoldItalic.ttf',
             'LiberationSans-Bold.ttf', 'LiberationSerif-Bold.ttf',
             'LiberationSans-Italic.ttf', 'LiberationSerif-Italic.ttf'
             'LiberationSansNarrow-BoldItalic.ttf', 'LiberationSerif-Regular.ttf']
    return('/usr/share/fonts/truetype/liberation/' + random.choice(fonts))


def text_as_image(width=200, height=200, text="Hello"):
    with Image(width=width, height=height) as img:
        font = Font(path=random_font_path_text(), color=Color(random_colour_text() ))
        img.caption(text,left=0,top=0,width=img.width-10,height=img.height-5,font=font,gravity='center')
        img.save(filename='200x100-transparent.png')
 
 
 
 
if __name__ == "__main__":
    text_as_image()


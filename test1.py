from wand.image import Image
from wand.drawing import Drawing
from wand.image import Font
from wand.color import Color
from wand.display import display

import random, tempfile, binascii



class imageInCardClass:
    def __init__(self, filenameImage, x, y):
        self.filenameImage = filenameImage
        self.x = x
        self.y = y
        self.percentageSize = random.randrange(50, 100, 5)
        self.rotation = random.randrange(0, 360, 5)
        print(self.filenameImage, self.x, self.y, self.percentageSize, self.rotation)

class cardClass:
    def __init__(self):
        self.images = []
        self.width=9000
        self.height=9000
        self.thumbWidth = 300
        self.thumbHeight = 300
        self.inspectWidth = 64
        self.inspectHeight = 64
        self.position = []
        self.widthSpace = self.width/3
        self.heightSpace = self.height/3
        self.inspectName = ''
        for x in range(0,3):
            for y in range(0,3):
                if x == 1 and y == 1:
                    pass # not the centre
                else:
                    self.position.append((x,y))
        random.shuffle(self.position)
        self.card = tempfile.NamedTemporaryFile(delete=False, suffix=".png")

    def newImage(self, filenameImage):
        index=len(self.images)
        x, y  = self.position[index]
        percentageSize = 100
        image = imageInCardClass(filenameImage, x*self.widthSpace , y*self.widthSpace)
        self.images.append(image)

    def full_card(self):
        with Image(width=self.width, height=self.height) as img:
            for index in range(0, len(self.images)):
                with Image(filename=self.images[index].filenameImage) as partImg:
                    img.composite(partImg, self.images[index].x , self.images[index].y)
            img.save(filename=self.card.name)
        print("Card: ", self.card.name)
        

    def thumbnail(self):
        thumbnail = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        thumbnailParts = []
        blob = None
        pixels = []
        partX = self.width/self.thumbWidth
        partY = self.height/self.thumbHeight
        for index in range(0, len(self.images)):
            part = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            with Image(filename=self.images[index].filenameImage) as img:
                img.resize((partX*self.images[index].percentageSize)/100,(partY*self.images[index].percentageSize)/100)
                thumbnailParts.append(part.name)
                img.save(filename=part.name)
        print("Thumbs", thumbnailParts)
        with Image(width=self.thumbWidth, height=self.thumbHeight) as img:
            for index in range(0, len(self.images)):
                with Image(filename=thumbnailParts[index]) as partImg:
                    img.composite(partImg, self.images[index].x / partX, self.images[index].y / partY)
            img.resize(self.inspectWidth, self.inspectHeight)
            img.save(filename=thumbnail.name)
            self.inspectName = thumbnail.name
            img.depth = 8
            blob = img.make_blob(format='RGB')

        # Iterate over blob and collect pixels
        for cursor in range(0, self.inspectWidth * self.inspectHeight * 3, 3):
            # Save tuple of color values
            p = binascii.b2a_hex((blob[cursor] + blob[cursor + 1] + blob[cursor + 2]))
            pixels.append(p)
        index = 0
        lastPixel = '000000'
        clash = False
        # Scan accross
        for x in range(0, self.inspectWidth):
            lastPixel = '000000'
            l = ""
            for y in range(0, self.inspectHeight):
               if pixels[index] == '000000':
                   l = l + "0"
                   lastPixel = '000000'
               else:
                   l = l + "1"
                   if lastPixel != '000000':
                       if pixels[index] != lastPixel:
                           clash = True
                   lastPixel = pixels[index]
               index = index + 1
            print l
        print("Clash :", clash)

#        print("Composite", thumbnail.name)




def random_colour_text():
#    colours = ['red', 'Maroon', 'Yellow', 'Olive', 'Lime', 'Green', 'Aqua', 'Teal', 'Purple']
#    return(random.choice(colours))
    r = random.randrange(0, 255, 1)
    g = random.randrange(0, 255, 1)
    b = random.randrange(0, 255, 1)
    colour = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ')'
    return(colour)

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


def text_as_image(width=1000, height=1000, text="Hello", filename="tmp.png"):
    with Image(width=width, height=height) as img:
        font = Font(path=random_font_path_text(), color=Color(random_colour_text() ))
        img.caption(text,left=0,top=0,width=img.width-10,height=img.height-5,font=font,gravity='center')
        img.rotate(random.randrange(0, 360, 5)) # Might make image bigger
        img.crop((img.width-width)/2, (img.height-height)/2, width+(img.width-width)/2, height+(img.height-height)/2)
        img.save(filename=filename)

def list_of_images_from_text(textList):
    images = []
    for text in textList:
        tf = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        text_as_image(text=text, filename=tf.name)
        images.append(tf.name)
    return images
 
def place_images_in_big_grid(images):
    card = cardClass()
    for image in images:
        card.newImage(image)
    card.thumbnail()
    card.full_card()
 
 
if __name__ == "__main__":
#    text_as_image(text="frefredfred")
    texts = ['Hello', 'world', 'domination']
    images = list_of_images_from_text(texts)
    print(images)
    place_images_in_big_grid(images)

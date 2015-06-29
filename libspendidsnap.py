from wand.image import Image
from wand.drawing import Drawing
from wand.image import Font
from wand.color import Color
from wand.display import display

import random, tempfile, binascii

class CardPosition:
    def __init__(self, position, thumb_filename):
        x, y  = position
        self.x = x 
        self.y = y 
        self.rotate = random.randrange(0, 360, 5)
        self.percentageSize = random.randrange(50, 100, 5)
        self.thumb = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        with Image(filename=thumb_filename) as img:
            with img[:, :] as duplicate:
                duplicate.rotate(self.rotate)
                duplicate.transform(resize=str(self.percentageSize)+'%')
                duplicate.save(filename=self.thumb.name)
        print("Card pos: ", self.thumb.name)


class Pack:
    def __init__(self, images_filenames_list):
        self.standard_width = 600
        self.thumb_width = 30
        self.card_width = self.standard_width * 3
        self.thumb_ext = '_thumb.png' 
        self.card_image_filenames_list = []
        self.images_filenames_list = []
        self.cards = []
        for images_filename in images_filenames_list:
            filename_copied = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            with Image(width=self.standard_width, height=self.standard_width) as img:
                with Image(filename=images_filename) as master_img:
                    if master_img.width > master_img.height:
                        master_img.transform(resize=self.standard_width)
                    else:
                        master_img.transform(resize='x' + str(self.standard_width))
                    img.composite(master_img, 0, 0)
                img.save(filename=filename_copied.name)
                # Thumbs
                if img.width > img.height:
                    img.transform(resize=self.thumb_width)
                else:
                    img.transform(resize='x' + str(self.thumb_width))
                img.save(filename=filename_copied.name + self.thumb_ext)
            self.images_filenames_list.append(filename_copied.name)
    def make_card(self, image_index_list):
        position = []
        for x in range(0,3):
            for y in range(0,3):
                if x == 1 and y == 1:
                    pass # not the centre
                else:
                    position.append((x,y))
        random.shuffle(position)
        card_positions = []
        for index in image_index_list:
            card_position = CardPosition(position[index], self.images_filenames_list[index]+self.thumb_ext)
            card_positions.append(card_position)
        return card_positions 



if __name__ == "__main__":
    i = ['/tmp/icons/anchor.png', '/tmp/icons/arrow.png', '/tmp/icons/circle.png']
    pack = Pack(i) 
    print(pack.images_filenames_list)
    card_positions = pack.make_card([0,1,2])


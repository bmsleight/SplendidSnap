from wand.image import Image
from wand.drawing import Drawing
from wand.image import Font
from wand.color import Color
from wand.display import display

import random, tempfile, binascii

class CardPosition:
    def __init__(self, position, thumb_filename, thumb_width):
        x, y  = position
        self.x = x * thumb_width
        self.y = y * thumb_width
        self.rotate = random.randrange(0, 360, 5)
        self.percentageSize = random.randrange(50, 95, 5)
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
        self.card_positions = []
        self.debug = True
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
            card_position = CardPosition(position[index], 
                                         self.images_filenames_list[index]+self.thumb_ext, 
                                         self.thumb_width)
            card_positions.append(card_position)
        self.card_positions = card_positions
        return card_positions
    def inspect_card_positions(self):
        thumbnail = tempfile.NamedTemporaryFile(delete=False, suffix="___.png")
        blob = None
        pixels = []
        with Image(width=self.thumb_width*3, height=self.thumb_width*3) as img:
            for card_position in self.card_positions:
                with Image(filename=card_position.thumb.name) as overlay:
                    img.composite(overlay, card_position.x, card_position.y)
            img.save(filename=thumbnail.name)
            img.depth = 8
            blob = img.make_blob(format='RGB')
        # Iterate over blob and collect pixels
        for cursor in range(0, (self.thumb_width*3) * (self.thumb_width*3) * 3, 3):
            # Save tuple of color values
            p = binascii.b2a_hex((blob[cursor] + blob[cursor + 1] + blob[cursor + 2]))
            pixels.append(p)
        index = 0
        lastPixel = '000000'
        clash = False
        # Scan accross
        for x in range(0, self.thumb_width*3):
            lastPixel = '000000'
            l = ""
            for y in range(0, self.thumb_width*3):
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
            if self.debug:
                print l
        if self.debug:
            print("Clash :", clash, thumbnail)

        # Up down
        index = 0
        lastPixel = '000000'
        for y in range(0, self.thumb_width*3):
            lastPixel = '000000'
            for x in range(0, self.thumb_width*3):
               if pixels[index] == '000000':
                   lastPixel = '000000'
               else:
                   if lastPixel != '000000':
                       if pixels[index] != lastPixel:
                           clash = True
                   lastPixel = pixels[index]
               index = index + 1
        if self.debug:
            print("Clash :", clash, thumbnail.name)
        return clash

    def move_closer(self):
        movement = False # No movements
        tmp_card_positions = self.card_positions
        inc = self.thumb_width / 10
        for index in range(0, len(self.card_positions)):
            x = self.card_positions[index].x
            if x > (self.thumb_width * 1.5):
                self.card_positions[index].x = self.card_positions[index].x - inc
            else:
                self.card_positions[index].x = self.card_positions[index].x + inc
            y = self.card_positions[index].y
            if y > (self.thumb_width * 1.5):
                self.card_positions[index].y = self.card_positions[index].y - inc
            else:
                self.card_positions[index].y = self.card_positions[index].y + inc
            if (self.inspect_card_positions()):
                # We have a clash with this move - revert
                self.card_positions[index].x = tmp_card_positions[index].x
                self.card_positions[index].y = tmp_card_positions[index].y
            else:
                movement = True
        print("Movement :", movement)
        return movement


if __name__ == "__main__":
    i = ['/tmp/icons/anchor.png', '/tmp/icons/arrow.png', '/tmp/icons/circle.png']
    pack = Pack(i) 
    print(pack.images_filenames_list)
    card_positions = pack.make_card([0,1,2])
    pack.inspect_card_positions()
    while(pack.move_closer()):
        pass


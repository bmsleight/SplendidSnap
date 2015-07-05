from wand.image import Image
from wand.drawing import Drawing
from wand.image import Font
from wand.color import Color
from wand.display import display

import random, tempfile, binascii

import time

class CardPosition:
    def __init__(self, position, thumb_filename, thumb_width):
        x, y  = position
        self.x = x * thumb_width
        self.y = y * thumb_width
        self.thumb_width = thumb_width
        self.rotate = random.randrange(0, 360, 5)
#        self.percentageSize = random.randrange(20, 90, 10)
        self.percentageSize = random.choice([45,60,75,80,85])
        self.thumb = tempfile.NamedTemporaryFile(delete=True, suffix=".png")
        self.thumb_as_list = []
        with Image(filename=thumb_filename) as img:
            with img[:, :] as duplicate:
                duplicate.rotate(self.rotate)
                duplicate.transform(resize=str(thumb_width)) # make sure still width s
                # + 5% to give space between images
                duplicate.transform(resize=str(self.percentageSize+15)+'%')

                # Using blob make in to a list of background vs image, 
                #  using 1 as some colour
                duplicate.depth = 8
                blob = duplicate.make_blob(format='RGB')
                for cursor in range(0, len(blob), 3):
                    if ((blob[cursor] + blob[cursor + 1] + blob[cursor + 2]) == '\x00\x00\x00'):
                        self.thumb_as_list.append(0)
                    else:
                        self.thumb_as_list.append(1)
#                if (True):


                self.thumb_width = duplicate.width # Newe resized width
#        print("Card positions ", self.x, self.y)
    def thumb_at_x_y(self, x, y):
        return(self.thumb_as_list[(x*self.thumb_width)+y])


class Pack:
    def __init__(self, images_filenames_list):
        self.standard_width = 600
        self.thumb_width = 30
        self.thumb_ratio = self.standard_width / self.thumb_width
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
                        master_img.transform(resize=str(self.standard_width))
                    else:
                        master_img.transform(resize='x' + str(self.standard_width))
                    img.composite(master_img, 0, 0)
                img.save(filename=filename_copied.name)
                if img.width > img.height:
                    img.transform(resize=str(self.thumb_width))
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
        self.card_positions = []
        p = 0
        for index in image_index_list:
            card_position = CardPosition(position[p], 
                                         self.images_filenames_list[index]+self.thumb_ext, 
                                         self.thumb_width)
            self.card_positions.append(card_position)
            p = p + 1
        #Squeeze them together 
        interactions = 0
        while(self.move_closer() and interactions < 150):
            interactions = interactions +1
        print interactions
        self.inspect_card_positions(display = True)
        with Image(width=self.card_width, height=self.card_width) as img:
            final_card = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
            card_index = 0 
            # the index refered to the long list of images [0,1,5,6]
            # card_index is to work through positions of the cards [0,1,2,3]
            for index in image_index_list:
                 with Image(filename=self.images_filenames_list[index]) as overlay:
                     # self.thumb_ratio
                     overlay.rotate(self.card_positions[card_index].rotate)
                     overlay.transform(resize=str(self.standard_width)) # make sure still width s
                     overlay.transform(resize=str(self.card_positions[card_index].percentageSize)+'%')
                     x = self.card_positions[card_index].x * self.thumb_ratio
                     y = self.card_positions[card_index].y * self.thumb_ratio
                     img.composite(overlay, x, y)
                 card_index = card_index + 1
            img.trim()
            with Image(width=self.card_width, height=self.card_width) as final_img:
                if img.width > img.height:
                    img.transform(resize=str(self.card_width))
                    final_img.composite(img, 0, (self.card_width - img.height)/2)
                    print(self.card_width - img.height, " ..")
                else:
                    img.transform(resize='x' + str(self.card_width))      
                    final_img.composite(img, (self.card_width - img.width)/2, 0)            
                    print(self.card_width - img.width)
                final_img.save(filename=final_card.name)

            self.cards.append(final_card.name)
            print("Final card: ", final_card.name)


    def inspect_card_positions(self, display = False):
        inspect_canvas = []
        # Canvas is three times bigger than thumb
        inspect_width = self.thumb_width*3
        clash = False
        for x in range(0, inspect_width):
            for y in range(0, inspect_width):
                inspect_canvas.append(0)
        for card_position in self.card_positions:
            pos_x_on_canvas = card_position.x 
            pos_y_on_canvas = card_position.y
#            print pos_x_on_canvas, pos_y_on_canvas, card_position.thumb_width
            for x in range(0, card_position.thumb_width):
                for y in range(0, card_position.thumb_width):
                    pixel = card_position.thumb_at_x_y(x,y)
                    inspect_x = pos_x_on_canvas + x
                    inspect_y = pos_y_on_canvas + y
#                    print inspect_x, inspect_y,x, y 
                    inspect_canvas[(inspect_x * inspect_width) + inspect_y] = inspect_canvas[(inspect_x * inspect_width) + inspect_y] + pixel
                    if inspect_canvas[(inspect_x * inspect_width) + inspect_y] > 1:
                        clash = True
        if (display):
            for x in range(0, inspect_width):
                g = ""
                for y in range(0, inspect_width):
                    g = g + str(inspect_canvas[(x * inspect_width) + y])
                print(g)
        return clash
    def move_closer(self):
        movement = False # No movements
        tmp_card_positions = self.card_positions
        inc = self.thumb_width / 10
#        inc = 1
        for index in range(0, len(self.card_positions)):
            x = self.card_positions[index].x
            if x > (self.thumb_width * 1.5):
                self.card_positions[index].x = self.card_positions[index].x - inc
            else:
                self.card_positions[index].x = self.card_positions[index].x + inc
            if (self.inspect_card_positions()):
                # We have a clash with this move - revert
                self.card_positions[index].x = x
#                print("REVERT")
            else:
                movement = True
        for index in range(0, len(self.card_positions)):
            y = self.card_positions[index].y
            if y > (self.thumb_width * 1.5):
                self.card_positions[index].y = self.card_positions[index].y - inc
            else:
                self.card_positions[index].y = self.card_positions[index].y + inc
            if (self.inspect_card_positions()):
                # We have a clash with this move - revert
                self.card_positions[index].y = y
#                print("REVERT")
            else:
                movement = True
#        print("Movement :", movement)
        return movement

	

#http://stackoverflow.com/questions/6240113/what-are-the-mathematical-computational-principles-behind-this-game
def simple_card_list(p):
    cards = []
    for i in range(p):
        pictures=[]
        for j in range(p):
            pictures.append(i * p + j)
        pictures.append(p*p)
        cards.append(pictures)
    for i in range(p):
        for j in range(p):
            pictures=[]
            for k in range(p):
                pictures.append(k * p + (j + i * k) % p)
            pictures.append(p * p + 1 + i)
            cards.append(pictures)
     
    pictures=[]
    for i in range(p+1):
        pictures.append(p * p + i)
    cards.append(pictures)
    return cards




if __name__ == "__main__":
 
    ii = ['/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Whale.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Raccoon.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Rhino.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Frog.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Penguin.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Koala.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Horse.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Snail.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Wolf.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Monkey.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Bee.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Bear.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Crocodile.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Lobster.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Kangaroo.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Mouse.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Goat.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Dolphin.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Octopus.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Rabbit.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Sheep.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Cat.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Elephant.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Beaver.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Bull.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Shark.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Chicken.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Crab.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Owl.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Gorilla.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Bat.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Hippo.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Pig.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Tuna.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Lion.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Cow.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Eagle.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Duck.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Snake.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Tiger.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Dog.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Deer.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Seal.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Squirrel.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Giraffe.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Turtle.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Rat.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Swan.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Lizard.png', '/home/bms/SplendidSnap/HTDFC-50-Animals-Square-PNG-Files/Fish.png']

    i = ['/tmp/icons/SplendidSnap.png', '/tmp/icons/anchor.png', '/tmp/icons/arrow.png', '/tmp/icons/circle.png', '/tmp/icons/triangle.png', '/tmp/icons/mouse.png', '/tmp/icons/dice.png']
    pack = Pack(ii) 
    print(pack.images_filenames_list)
#    card_positions = pack.make_card([0,1,2,3,4,5,6])
    arrangements = simple_card_list(6)[16:24]
    for arrangement in arrangements:
        pack.make_card(arrangement)
    print arrangements
    print pack.cards
#    pack.inspect_card_positions()



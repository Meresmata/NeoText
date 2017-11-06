# writing texts with neopixels 8x8 matrices
"""
 Test file to write text on neopixel matrixes
"""
import gc
from board import *
# import adafruit_dotstar as dotstar
# import time
import neopixel

def colorintensity(color, percentage):
    red = (color & 0xFF0000)>>16
    green = color & 0x00FF00>>8
    blue = color & 0x0000FF

    red = int((red * percentage)/100)
    green = int((green * percentage)/100)
    blue = int((blue * percentage)/100)

    return red<<16 | green << 8 |blue


def square(base):
    """
    param base: base to be squared
    return: int
    """
    return int(pow(base, 2))

maxindex = 255
offset = 0
Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890/\ ?.!:; abcdefghijklmnopqrstuvwxyz"


def mapled(position, in_offset, orientation="Line"):
    """

    :param position: tuple of two ints
    :param in_offset: int
    :param orientation: string
    :return: int
    """
    tilesize = 8
    maxindex = tilesize - 1
    x_val, y_val = position
    try:
        orientation.isalpha()
    except(RuntimeError, TypeError):
        print("orientation is not a string.")

    orientation = orientation.upper()
    matrixnumber = (in_offset + x_val) // tilesize

    if (orientation == "ZICZAC") and (matrixnumber % 2):
        matrixpos = (in_offset + x_val) % tilesize + tilesize * y_val
    else:
        matrixpos = (maxindex - y_val) + tilesize * ((x_val + in_offset) % tilesize)
    return square(tilesize) * matrixnumber + matrixpos


WHITE = 0xffffff
RED = 0xff0000


def getpixel(letter, in_offset):
    """

    :type letter: Char
    :type in_offset: int (positive)
    :return: tupel of tupel, int
    """
    if letter in Alphabet:
        if letter == "H":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 3), (2, 3), (3, 3), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6))
        elif letter == "I":
            in_offset += 2
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6))
        elif letter == "J":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 5), (1, 0), (1, 6), (2, 0), (2, 6), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5))
        elif letter == "K":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 3), (2, 2), (2, 4), (3, 0), (3, 1), (3, 5), (3, 6))
        elif letter == "L":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6))
        elif letter == "M":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 1), (1, 2), (2, 3), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 4), (4, 5), (4, 6))
        elif letter == "N":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 1), (1, 2), (2, 3), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "O":
            in_offset += 6
            rtuple = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 1), (1, 5), (1, 6), (2, 0), (2, 6), (3, 0), (3, 1), (3, 5), (3, 6), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5))
        elif letter == "P":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 3), (2, 0), (2, 3), (3, 0), (3, 3), (4, 1), (4, 2))
        elif letter == "P":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 2), (2, 0), (2, 2), (3, 0), (3, 2), (4, 1), (4, 2))
        elif letter == "Q":
            in_offset += 6
            rtuple = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 1), (1, 5), (1, 6), (2, 0), (2, 4), (2, 6), (3, 0), (3, 1), (3, 5), (4, 1), (4, 2), (4, 3), (4, 4), (4, 6))
        elif letter == "R":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 3), (2, 0), (2, 3), (2, 4), (2, 6), (3, 1), (3, 2), (3, 5), (3, 6))
        elif letter == "S":
            in_offset += 6
            rtuple = ((0, 1), (0, 2), (0, 5), (1, 0), (1, 2), (1, 6), (2, 0), (2, 3), (2, 6), (3, 0), (3, 4), (3, 6), (4, 1),(4, 4), (4, 5))
        elif letter == "T":
            in_offset += 6
            rtuple = ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 0), (4, 0))
        elif letter == "U":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (1, 6), (2, 4), (2, 5), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "V":
            in_offset += 6
            rtuple = ((0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 6), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (4, 0))
        elif letter == "W":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (1, 5), (1, 6), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 4), (3, 5), (3, 6), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4))
        elif letter == "X":
            in_offset += 5
            rtuple = ((0, 0), (0, 6), (1, 1), (1, 2), (1, 4), (1, 5), (1, 0), (2, 3), (3, 1), (3, 2), (3, 4), (3, 5), (4, 5), (4, 6))
        elif letter == "Y":
            in_offset += 5
            rtuple = ((0, 0), (1, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 0), (3, 1))
        elif letter == "Z":
            in_offset += 6
            rtuple = ((0, 0), (0, 5), (0, 6), (1, 0), (1, 3), (1, 4), (2, 0), (2, 2), (2, 3), (2, 6), (3, 0), (3, 1), (3, 3), (3, 6), (4, 0), (4, 1), (4, 6))
        else:
            rtuple = (())
        return rtuple, in_offset


# starting of the main programm
NUMPIXELS = 4*64
neopixels = neopixel.NeoPixel(D4, NUMPIXELS, auto_write=False)
intensity = 5

def run():
    global offset
    for letter in "TUVW":
        pixels, next_offset = getpixel(letter, offset)
        print(letter)
        print(pixels)

        for pixel in pixels:
            pos = mapled(pixel, offset, "ZICZAC")
            gc.collect()
            if pos > maxindex:
                break
            elif pos < 0:
                continue
            else:
                print(pos)
                neopixels[pos] = colorintensity(WHITE, intensity)
        offset = next_offset


    neopixels.show()



if __name__ == "__main__":
    run()

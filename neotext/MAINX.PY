    # writing texts with neopixels 8x8 matrices

from board import *
# import adafruit_dotstar as dotstar
# import time
import neopixel


def square(x):
    return pow(x, 2)

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
    finally:
        "orientation is not a string."

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
        if letter == "A":
            in_offset += 8
            print(in_offset)
            rtuple = ((0, 6), (1, 4), (1, 5), (1, 6), (2, 1), (2, 2), (2, 3), (3, 0), (3, 3), (4, 0), (4, 3), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (6, 6))
        elif letter == "B":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 3), (1, 6), (2, 0), (2, 3), (2, 6), (3, 0), (3, 3), (3, 6), (4, 1), (4, 2), (4, 4), (4, 5))
        elif letter == "C":
            in_offset += 6
            rtuple = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 1), (1, 5), (1, 6), (2, 0), (2, 6), (3, 0), (3, 6), (4, 1), (4, 5))
        elif letter == "D":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 6), (2, 0), (2, 6), (3, 1), (3, 5), (4, 2), (4, 3), (4, 4))
        elif letter == "E":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 3), (1, 6), (2, 0), (2, 3), (2, 6), (3, 0), (3, 6))
        elif letter == "F":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 3), (2, 0), (2, 3), (3, 0))
        elif letter == "G":
            in_offset += 6
            rtuple = ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 6), (2, 0), (2, 4), (2, 6), (3, 0), (3, 4), (3, 5), (4, 1), (4, 2), (4, 4), (4, 5), (4, 6))
        elif letter == "H":
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
            rtuple = ((0, 0), (0, 1), (0, 2), (0,3), (0, 4), (0, 5), (0, 6), (1, 3), (2, 2), (2, 4), (3, 0), (3, 1), (3, 5), (3, 6))
        elif letter == "L":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0,3), (0, 4), (0, 5), (0, 6), (1, 6), (2, 6), (3, 6))
        elif letter == "M":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0,3), (0, 4), (0, 5), (0, 6), (1, 1), (1, 2), (2, 3), (3, 1), (3, 2), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 4), (4, 5), (4, 6))
        elif letter == "N":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0,3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 1), (2, 2), (2, 2), (2, 4), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "O":
            in_offset += 6
            rtuple = ((0, 1), (0, 2), (0,3), (0, 4), (0, 5),(1, 0), (1, 1), (1, 5), (1, 6), (2, 0), (2, 6), (3, 0), (3, 1), (3, 2), (3, 5), (3, 6), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5))
        elif letter == "P":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0,3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 3), (2, 0), (2, 3), (3, 0), (3, 3), (4, 1), (4, 2))
        elif letter == "P":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0,3), (0, 4), (0, 5),(0, 6), (1, 0), (1, 2), (2, 0), (2, 2), (3, 0), (3, 2), (4, 1), (4, 2))
        elif letter == "Q":
            in_offset += 6
            rtuple = ((0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 5), (1, 6), (2, 0), (2, 4), (2, 6), (3, 0), (3, 1), (3, 5), (4, 1), (4, 2), (4, 3), (4, 4), (4, 6))
        elif letter == "R":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 0), (1, 3), (2, 0), (2, 3), (2, 4), (2, 6), (3, 1),(3, 2), (3, 5), (3, 6))
        elif letter == "S":
            in_offset += 6
            rtuple = ((0, 1), (0, 2), (0, 5), (1, 0), (1, 2), (1, 6), (2, 0), (2, 3), (2, 6), (3, 0), (3, 4), (3, 6), (4, 1), (4, 4), (4, 5))
        elif letter == "T":
            in_offset += 6
            rtuple = ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 0), (4, 0))
        elif letter == "U":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (1, 6), (2, 4), (2, 5), (3, 0), (3, 1),(3, 2), (3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "V":
            in_offset += 6
            rtuple = ((0, 0), (1, 0), (1, 1), (1,2), (1, 3), (1, 4),(1, 5), (2, 6), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (4, 0))
        elif letter == "W":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (1, 5), (1, 6), (2, 0), (2, 1), (2, 3),(2, 4),  (3, 0), (3, 4), (3, 5), (3, 6), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4))
        elif letter == "X":
            in_offset += 5
            rtuple = ((0, 0), (0, 6), (1, 1), (1, 2), (1, 4), (1, 5), (1, 0), (2, 3), (3, 1), (3, 2), (3, 4), (3, 5), (4, 5),(4, 6))
        elif letter == "Y":
            in_offset += 5
            rtuple = ((0, 0), (1, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (3, 0), (3, 1))
        elif letter == "Z":
            in_offset += 6
            rtuple = ((0, 0), (0, 5), (0, 6), (1, 0), (1, 3), (1, 4), (2, 0), (2, 2), (2, 3), (2, 6), (3, 0), (3, 1), (3, 3), (3, 6), (4, 0), (4, 1), (4, 6))
        elif letter == "1":
            in_offset += 5
            rtuple = ((0, 2), (1, 1), (2, 0), (2, 1), (3, 0, (3, 1), (3, 2), 3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "2":
            in_offset += 6
            rtuple = ((0, 1), (0, 6), (1, 0), (1, 5), (1, 6), (2, 0), (2, 5), (2, 6), (3, 0), (3, 3), (3, 4), (3, 6), (4, 1), (4, 2), (4, 6))
        elif letter == "3":
            in_offset += 7
            rtuple = ((0, 0), (0, 3), (0, 6), (1, 0), (1,3), (1, 6), (2, 0), (2, 2), (2, 3), (2, 6), (3, 1), (3, 2), (3, 4), (3, 5))
        elif letter == "4":
            in_offset += 6
            rtuple = ((0,0), (0,1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "5":
            in_offset += 6
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 5), (0, 6), (1, 0), (1, 4), (1, 6), (2, 0), (2, 4), (2, 5),  (2, 6), (3, 0), (3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "6":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 3), (1, 6), (2, 0), (2, 3), (2, 6), (3, 0), (3, 1), (3, 4), (3, 5))
        elif letter == "7":
            in_offset += 5
            rtuple = ((0, 0), (0, 3), (0, 5), (0, 6), (1, 0), (1, 3), (1, 4), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 3))
        elif letter == "8":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 3), (1, 6), (2, 0), (3, 3), (2, 6), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),(3, 6))
        elif letter == "9":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 5), (0, 6), (1, 0), (1, 3), (1, 6), (2, 0), (2, 3), (2, 6), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),(3, 6))
        elif letter == "0":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 5), (0, 6), (1, 0), (1, 6), (2, 0), (2, 6), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),(3, 6))
        elif letter == "/":
            in_offset += 4
            rtuple = ((0, 5), (0, 6), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1))
        elif letter == "\\":
            in_offset += 4
            rtuple = ((0, 0), (0, 1), (0, 6), (1, 1), (1, 2), (1, 3), (2, 3), (2, 4), (2, 4), (3, 5), (3, 6))
        elif letter == "?":
            in_offset += 4
            rtuple = ((0, 0), (0, 1), (0, 3), (1, 0), (1, 2), (1, 4), (1, 6), (2, 0), (2, 1), (2, 3), (2, 4))
        elif letter == ".":
            in_offset += 2
            rtuple = ((0, 6))
        elif letter == "!":
            in_offset += 2
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 6))
        elif letter == ":":
            in_offset += 5
            rtuple = ((0, 3), (0, 5))
        elif letter == ",":
            in_offset += 2
            rtuple = ((0, 6), (0, 7), (1, 5), (0, 6))
        elif letter == ";":
            in_offset += 4
            rtuple = ((0, 6), (0, 7), (1, 5), (1, 6), (2, 3))
        elif letter == "a":
            in_offset += 6
            rtuple = ((0, 4), (0, 5), (1, 3), (1, 6), (2, 3), (2, 6), (3, 4), (3, 5), (3, 6), (4, 3), (4, 4), (4, 5), (4, 6))
        elif letter == "b":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 4), (1, 6), (2, 3), (2, 6), (3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "c":
            in_offset += 4
            rtuple = ((0, 4), (0, 5), (1, 3), (1, 6), (2, 3), (2, 6))
        elif letter == "d":
            in_offset += 5
            rtuple = ((0, 4), (0, 5), (1, 3), (1, 6), (2, 4), (2, 5), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "e":
            in_offset += 5
            rtuple = ((0, 3), (0, 4), (0, 5), (1, 2), (1, 4), (1, 6), (2, 2), (2, 4), (2, 6), (3, 3), (3, 4), (3, 6))
        elif letter == "f":
            in_offset += 5
            rtuple = ((0, 3), (1, 0), (1, 1), (1, 2), (1, 4), (1, 5), (1, 6), (2, 0), (2, 3), (3, 0))
        elif letter == "g":
            in_offset += 4
            rtuple = ((0, 3), (0, 4), (0, 5), (0, 7), (1, 3), (1, 5), (1, 7), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7))
        elif letter == "h":
            in_offset += 4
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 3), (2, 3), (3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "i":
            in_offset += 6
            rtuple = ((0, 1), (0, 3), (0, 4), (0, 5), (0, 6))
        elif letter == "j":
            in_offset += 5
            rtuple = ((0, 7), (0, 1), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7))
        elif letter == "k":
            in_offset += 4
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 5), (2, 3), (2, 4), (2, 6))
        elif letter == "l":
            in_offset += 5
            rtuple = ((0, 0), (0, 1), (0, 2), (0, 3),  (0, 4), (0, 5), (0, 6), (1, 6))
        elif letter == "m":
            in_offset += 6
            rtuple = ((0, 3), (0, 4), (0, 5), (0, 6), (1, 4), (2, 4), (2, 5), (2, 6), (3, 4), (4, 4), (4, 5), (4, 6))
        elif letter == "n":
            in_offset += 4
            rtuple = ((0, 3), (0, 4), (0, 5), (0, 6), (1, 4), (2, 4), (2, 5), (2, 6))
        elif letter == "o":
            in_offset += 4
            rtuple = ((0, 4), (0, 5), (1, 3), (1, 6), (2, 4), (2, 5))
        elif letter == "p":
            in_offset += 5
            rtuple = ((0, 3), (0, 4), (0, 5), (0, 6), (1, 3), (1, 5), (2, 3), (2, 5), (3, 4))
        elif letter == "q":
            in_offset += 6
            rtuple = ((0, 4), (1, 3), (1, 5), (2, 3), (2, 5), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7))
        elif letter == "r":
            in_offset += 4
            rtuple = ((0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 4), (2, 3))
        elif letter == "s":
            in_offset += 4
            rtuple = ((0, 3), (0, 4), (0, 6), (1, 3), (1, 4), (1, 5), (2, 3), (2, 5), (2, 6))
        elif letter == "t":
            in_offset += 4
            rtuple = ((0, 2), (1, 0) (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 2))
        elif letter == "u":
            in_offset += 5
            rtuple = ((0, 3), (0, 4), (0, 5), (1, 6), (2, 5), (3, 3), (3, 4), (3, 5), (3, 6))
        elif letter == "v":
            in_offset += 4
            rtuple = ((0, 3), (0, 4), (1, 5), (1, 6), (2, 3), (2, 4))
        elif letter == "w":
            in_offset += 6
            rtuple = ((0, 3), (0, 4), (1, 5), (1, 6), (2, 4), (3, 5), (3, 6), (4, 3), (4, 4))
        elif letter == "x":
            in_offset += 4
            rtuple = ((0, 3), (0, 4), (1, 5), (1, 6), (3, 5), (3, 6), (4, 3), (4, 4))
        elif letter == "y":
            in_offset += 4
            rtuple = ((0, 3), (0, 4), (0, 5), (0,7), (1, 7), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7))
        elif letter == "z":
            in_offset += 5
            rtuple = ((0, 3), (0, 6), (1, 3), (1, 5), (2, 3), (2, 4), (2, 6), (3, 3), (3, 6))
        else:
            rtuple = (())
        return rtuple, in_offset


# starting of the main programm
NUMPIXELS = 4*64
neopixels = neopixel.NeoPixel(D4, NUMPIXELS, brightness=0.1, auto_write=False)


def run():
    global offset
    for letter in "ABCDEF":
        pixels, next_offset = getpixel(letter, offset)
        print(letter)
        print(pixels)

        for pixel in pixels:
            pos = mapled(pixel, offset, "ZICZAC")
            if pos > maxindex:
                break
            elif pos < 0:
                continue
            else:
                print(pos)
                neopixels[pos] = WHITE
        offset = next_offset
    neopixels.show()


if __name__ == "__main__":
    run()

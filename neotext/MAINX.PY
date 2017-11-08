"""
writing texts with up to 4  chained neopixel 8x8 matrices
"""
import gc
import array as a
from board import *
import neopixel


MAXINDEX = 255
offset = 0
# ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890/\\ ?.!:;abcdefghijklmnopqrstuvwxyz"

# starting of the main programm
NUMPIXELS = 4*64
neopixels = neopixel.NeoPixel(D4, NUMPIXELS, auto_write=False)
INTENSITY = 5# in percent

WHITE = 0xffffff
RED = 0xff0000
BLUE = 0x0000
YELLOW = 0xffff00
CYAN = 0x00ffff
MAGENTA = 0xff00ff
ORANGE = 0xffa500
GREEN = 0x00FF00
BLACK = 0x000000


def colorINTENSITY(color, percentage):
    """
    calculates the 24 bit color from a param color and param percentage (0.0 - 100.0)
    param color: int
    param percentage: float
    return: int
    """
    red = (color & 0xFF0000)>>16
    green = color & 0x00FF00>>8
    blue = color & 0x0000FF

    red = int((red * percentage)/100)
    green = int((green * percentage)/100)
    blue = int((blue * percentage)/100)

    return red<<16 | green << 8 |blue


def square(base):
    """
    squares param base
    param base: base to be squared
    return: int
    """
    return int(pow(base, 2))


def mapled(x_coord, y_coord, in_offset, orientation="Line"):
    """
    map the position of the LED positions to the led numbers
    :param x_coord: int
    :param y_coord: int
    :param in_offset: int
    :param orientation: string
    :return: int
    """
    TILESIZE = 8
    MAXINDEX = TILESIZE - 1
    try:
        orientation.isalpha()
    except(RuntimeError, TypeError):
        print("orientation is not a string.")

    orientation = orientation.upper()
    print(orientation)
    matrixnumber = (in_offset + x_coord) // TILESIZE
    print(matrixnumber)

    if (orientation == "ZICZAC") and (matrixnumber % 2):
        matrixpos = (in_offset + x_coord) % TILESIZE + TILESIZE * y_coord
        print(matrixpos)
    else:
        matrixpos = (MAXINDEX - y_coord) + TILESIZE * ((x_coord + in_offset) % TILESIZE)
        print(matrixpos)
    return square(TILESIZE) * matrixnumber + matrixpos


def getpixel(letter, in_offset):
    """
    get the LED position for a given sign/character
    :type letter: Char
    :type in_offset: int (positive)
    :return: tupel of tupel, int
    """
    if ord(letter) < 128:#if is ascii
        if letter.isalpha() and letter.isupper():
            rtuple, r_offset = _getpixel_from_ABC(letter, in_offset)
        elif letter.isalpha() and letter.islower():
            rtuple, r_offset = _getpixel_from_abc(letter, in_offset)
        elif letter.isdecimal():
            rtuple, r_offset = _getpixel_from_dec(letter, in_offset)
        elif letter in "/\\ ?.!:;":
            rtuple, r_offset = _getpixel_from_special(letter, in_offset)
        else:
            rtuple = a.array("B", ())
            r_offset = 0
        return rtuple, in_offset + r_offset


def _getpixel_from_ABC(letter, in_offset):
    """
    get the LED position for a given sign/character
    :type letter: Char
    :type in_offset: int (positive)
    :retval: tupel of tupel, int
    """
    if letter == "A":
        in_offset += 8
        print(in_offset)
        rtuple = a.array("B", (0, 6, 1, 4, 1, 5, 1, 6, 2, 1, 2, 2, 2, 3, 3, 0, 3, 3, 4, 0, 4, 3, 5, 1, 5, 2, 5, 3, 5, 4, 5, 5, 5, 6, 6, 6))
    elif letter == "B":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 3, 3, 6, 4, 1, 4, 2, 4, 4, 4, 5))
    elif letter == "C":
        in_offset += 6
        rtuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 1, 0, 1, 1, 1, 5, 1, 6, 2, 0, 2, 6, 3, 0, 3, 6, 4, 1, 4, 5))
    elif letter == "D":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 0, 1, 6, 2, 0, 2, 6, 3, 1, 3, 5, 4, 2, 4, 3, 4, 4))
    elif letter == "E":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 6))
    elif letter == "F":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 0, 1, 3, 2, 0, 2, 3, 3, 0))
    elif letter == "G":
        in_offset += 6
        rtuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 1, 0, 1, 6, 2, 0, 2, 4, 2, 6, 3, 0, 3, 4, 3, 5, 4, 1, 4, 2, 4, 4, 4, 5, 4, 6))
    elif letter == "H":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 3, 2, 3, 3, 3, 4, 0, 4, 1, 4, 2, 4, 3, 4, 4, 4, 5, 4, 6))
    elif letter == "I":
        in_offset += 2
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6))
    elif letter == "J":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 5, 1, 0, 1, 6, 2, 0, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5))
    elif letter == "K":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 3, 2, 2, 2, 4, 3, 0, 3, 1, 3, 5, 3, 6))
    elif letter == "L":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 6, 2, 6, 3, 6))
    elif letter == "N":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 1, 1, 2, 2, 3, 2, 4, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "O":
        in_offset += 6
        rtuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 1, 0, 1, 1, 1, 5, 1, 6, 2, 0, 2, 6, 3, 0, 3, 1, 3, 5, 3, 6, 4, 1, 4, 2, 4, 3, 4, 4, 4, 5))
    elif letter == "P":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 0, 1, 3, 2, 0, 2, 3, 3, 0, 3, 3, 4, 1, 4, 2))
    elif letter == "Q":
        in_offset += 6
        rtuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 1, 0, 1, 1, 1, 5, 1, 6, 2, 0, 2, 4, 2, 6, 3, 0, 3, 1, 3, 5, 4, 1, 4, 2, 4, 3, 4, 4, 4, 6))
    elif letter == "R":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 1, 0, 1, 3, 2, 0, 2, 3, 2, 4, 2, 6, 3, 1, 3, 2, 3, 5, 3, 6))
    elif letter == "S":
        in_offset += 6
        rtuple = a.array("B", (0, 1, 0, 2, 0, 5, 1, 0, 1, 2, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 4, 3, 6, 4, 1, 4, 4, 4, 5))
    elif letter == "T":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 1, 0, 2, 0, 2, 1, 2, 2, 2, 3, 2, 4, 2, 5, 2, 6, 3, 0, 4, 0))
    elif letter == "U":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 1, 5, 1, 6, 2, 4, 2, 5, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "V":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 1, 0, 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 4, 0))
    elif letter == "W":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 1, 4, 1, 5, 1, 6, 2, 0, 2, 1, 2, 3, 2, 4, 3, 0, 3, 4, 3, 5, 3, 6, 4, 0, 4, 1, 4, 2, 4, 3, 4, 4))
    elif letter == "X":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 6, 1, 1, 1, 2, 1, 4, 1, 5, 1, 0, 2, 3, 3, 1, 3, 2, 3, 4, 3, 5, 4, 5, 4, 6))
    elif letter == "Y":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 1, 1, 2, 2, 2, 3, 2, 4, 2, 5, 2, 6, 3, 0, 3, 1))
    elif letter == "Z":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 0, 5, 0, 6, 1, 0, 1, 3, 1, 4, 2, 0, 2, 2, 2, 3, 2, 6, 3, 0, 3, 1, 3, 3, 3, 6, 4, 0, 4, 1, 4, 6))
    else:
        rtuple = a.array("B", ())
    return rtuple, in_offset


def _getpixel_from_dec(letter, in_offset):
    """
    get the LED position for a given sign/character
    :type letter: Char
    :type in_offset: int (positive)
    :retval: tupel of tupel, int
    """
    if letter == "1":
        in_offset += 5
        rtuple = a.array("B", (0, 2, 1, 1, 2, 0, 2, 1, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "2":
        in_offset += 6
        rtuple = a.array("B", (0, 1, 0, 6, 1, 0, 1, 5, 1, 6, 2, 0, 2, 5, 2, 6, 3, 0, 3, 3, 3, 4, 3, 6, 4, 1, 4, 2, 4, 6))
    elif letter == "3":
        in_offset += 7
        rtuple = a.array("B", (0, 0, 0, 3, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 2, 2, 3, 2, 6, 3, 1, 3, 2, 3, 4, 3, 5))
    elif letter == "4":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 1, 4, 2, 4, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "5":
        in_offset += 6
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 5, 0, 6, 1, 0, 1, 4, 1, 6, 2, 0, 2, 4, 2, 5, 2, 6, 3, 0, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "6":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 1, 3, 4, 3, 5))
    elif letter == "7":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 3, 0, 5, 0, 6, 1, 0, 1, 3, 1, 4, 2, 0, 2, 1, 2, 2, 2, 3, 3, 0, 3, 1, 3, 3))
    elif letter == "8":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 3, 3, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "9":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "0":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 5, 0, 6, 1, 0, 1, 6, 2, 0, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    else:
        rtuple = a.array("B", ())
    return rtuple, in_offset


def _getpixel_from_special(letter, in_offset):
    """
    get the LED position for a given sign/character
    :type letter: Char
    :type in_offset: int (positive)
    :retval: tupel of tupel, int
    """
    if letter == "/":
        in_offset += 4
        rtuple = a.array("B", (0, 5, 0, 6, 1, 3, 1, 4, 1, 5, 2, 1, 2, 2, 2, 3, 3, 0, 3, 1))
    elif letter == "\\":
        in_offset += 4
        rtuple = a.array("B", (0, 0, 0, 1, 0, 6, 1, 1, 1, 2, 1, 3, 2, 3, 2, 4, 2, 4, 3, 5, 3, 6))
    elif letter == "?":
        in_offset += 4
        rtuple = a.array("B", (0, 0, 0, 1, 0, 3, 1, 0, 1, 2, 1, 4, 1, 6, 2, 0, 2, 1, 2, 3, 2, 4))
    elif letter == ".":
        in_offset += 2
        rtuple = a.array("B", (0, 6))
    elif letter == "!":
        in_offset += 2
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 6))
    elif letter == ":":
        in_offset += 5
        rtuple = a.array("B", (0, 3, 0, 5))
    elif letter == ",":
        in_offset += 2
        rtuple = a.array("B", (0, 6, 0, 7, 1, 5, 0, 6))
    elif letter == ";":
        in_offset += 4
        rtuple = a.array("B", (0, 6, 0, 7, 1, 5, 1, 6, 2, 3))
    else:
        rtuple = a.array("B", ())
    return rtuple, in_offset



def _getpixel_from_abc(letter, in_offset):
    """
    get the LED position for a given sign/character
    :type letter: Char
    :type in_offset: int (positive)
    :retval: tupel of tupel, int
    """
    if letter == "a":
        in_offset += 6
        rtuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 2, 3, 2, 6, 3, 4, 3, 5, 3, 6, 4, 3, 4, 4, 4, 5, 4, 6))
    elif letter == "b":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 4, 1, 6, 2, 3, 2, 6, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "c":
        in_offset += 4
        rtuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 2, 3, 2, 6))
    elif letter == "d":
        in_offset += 5
        rtuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 2, 4, 2, 5, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "e":
        in_offset += 5
        rtuple = a.array("B", (0, 3, 0, 4, 0, 5, 1, 2, 1, 4, 1, 6, 2, 2, 2, 4, 2, 6, 3, 3, 3, 4, 3, 6))
    elif letter == "f":
        in_offset += 5
        rtuple = a.array("B", (0, 3, 1, 0, 1, 1, 1, 2, 1, 4, 1, 5, 1, 6, 2, 0, 2, 3, 3, 0))
    elif letter == "g":
        in_offset += 4
        rtuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 7, 1, 3, 1, 5, 1, 7, 2, 3, 2, 4, 2, 5, 2, 6, 2, 7))
    elif letter == "h":
        in_offset += 4
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 3, 2, 3, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "i":
        in_offset += 6
        rtuple = a.array("B", (0, 1, 0, 3, 0, 4, 0, 5, 0, 6))
    elif letter == "j":
        in_offset += 5
        rtuple = a.array("B", (0, 7, 0, 1, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7))
    elif letter == "k":
        in_offset += 4
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 5, 2, 3, 2, 4, 2, 6))
    elif letter == "l":
        in_offset += 5
        rtuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 6))
    elif letter == "m":
        in_offset += 6
        rtuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 1, 4, 2, 4, 2, 5, 2, 6, 3, 4, 4, 4, 4, 5, 4, 6))
    elif letter == "n":
        in_offset += 4
        rtuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 1, 4, 2, 4, 2, 5, 2, 6))
    elif letter == "o":
        in_offset += 4
        rtuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 2, 4, 2, 5))
    elif letter == "p":
        in_offset += 5
        rtuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 1, 3, 1, 5, 2, 3, 2, 5, 3, 4))
    elif letter == "q":
        in_offset += 6
        rtuple = a.array("B", (0, 4, 1, 3, 1, 5, 2, 3, 2, 5, 3, 3, 3, 4, 3, 5, 3, 6, 3, 7))
    elif letter == "r":
        in_offset += 4
        rtuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 1, 4, 2, 3))
    elif letter == "s":
        in_offset += 4
        rtuple = a.array("B", (0, 3, 0, 4, 0, 6, 1, 3, 1, 4, 1, 5, 2, 3, 2, 5, 2, 6))
    elif letter == "t":
        in_offset += 4
        rtuple = a.array("B", (0, 2, 1, 0, 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 2, 2))
    elif letter == "u":
        in_offset += 5
        rtuple = a.array("B", (0, 3, 0, 4, 0, 5, 1, 6, 2, 5, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "v":
        in_offset += 4
        rtuple = a.array("B", (0, 3, 0, 4, 1, 5, 1, 6, 2, 3, 2, 4))
    elif letter == "w":
        in_offset += 6
        rtuple = a.array("B", (0, 3, 0, 4, 1, 5, 1, 6, 2, 4, 3, 5, 3, 6, 4, 3, 4, 4))
    elif letter == "x":
        in_offset += 4
        rtuple = a.array("B", (0, 3, 0, 4, 1, 5, 1, 6, 3, 5, 3, 6, 4, 3, 4, 4))
    elif letter == "y":
        in_offset += 4
        rtuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 7, 1, 7, 2, 3, 2, 4, 2, 5, 2, 6, 2, 7))
    elif letter == "z":
        in_offset += 5
        rtuple = a.array("B", (0, 3, 0, 6, 1, 3, 1, 5, 2, 3, 2, 4, 2, 6, 3, 3, 3, 6))
    else:
        rtuple = a.array("B", ())
    return rtuple, in_offset


def restart(in_num):
    """
    Resetting the global offset value to inNum
    param inNum: int
    retval: none
    """
    global offset
    offset = in_num
    for index in range(0, NUMPIXELS):
        neopixels[index] = colorINTENSITY(BLACK, 100.0)
        print(str(index) + " " + str(colorINTENSITY(BLACK, 100.0)))
    neopixels.show()


def write(text):
    """
    Writes the param to the Neopixel Matrix
    param text: string
    retval: none
    """
    global offset
    for letter in text:
        pixels, next_offset = getpixel(letter, offset)
        print(letter)
        print(pixels)
        write_raw(pixels)
        offset = next_offset

def write_raw(raw_position_list, orientation="ZICZAC"):
    """
    param raw_position_list: array (of bytes)
    param orientation: orientation of the matrices towards each other
    retval: none
    """
    global offset
    for index in range(0, len(raw_position_list), 2):
        x_pos = raw_position_list[index]
        y_pos = raw_position_list[index+1]
        pos = mapled(x_pos, y_pos, offset, orientation)
        gc.collect()
        if pos > NUMPIXELS-1:
            break
        elif pos < 0:
            continue
        else:
            print(pos)
            neopixels[pos] = colorINTENSITY(WHITE, INTENSITY)
    neopixels.show()


if __name__ == "__main__":
    write("A")

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
# INTENSITY = 5  # in percent

WHITE = 0xffffff
RED = 0xff0000
BLUE = 0x0000
YELLOW = 0xffff00
CYAN = 0x00ffff
MAGENTA = 0xff00ff
ORANGE = 0xffa500
GREEN = 0x00FF00
BLACK = 0x000000


def color_intensity(color, percentage):
    """
    calculates the 24 bit color from a param
    color and param percentage (0.0 - 100.0)
    param color: int
    param percentage: float
    return: int
    """
    red = (color & 0xFF0000) >> 16
    green = color & 0x00FF00 >> 8
    blue = color & 0x0000FF

    red = int((red * percentage)/100)
    green = int((green * percentage)/100)
    blue = int((blue * percentage)/100)

    return red << 16 | green << 8 | blue


def square(base):
    """
    squares param base
    param base: base to be squared
    return: int
    """
    return int(pow(base, 2))


def map_led(x_coord, y_coord, in_offset, orientation="Line"):
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
    matrix_number = (in_offset + x_coord) // TILESIZE
    print(matrix_number)

    if (orientation == "ZICZAC") and (matrix_number % 2):
        matrix_pos = (in_offset + x_coord) % TILESIZE + TILESIZE * y_coord
        print(matrix_pos)
    else:
        matrix_pos = (MAXINDEX - y_coord) + TILESIZE * ((x_coord + in_offset) % TILESIZE)
        print(matrix_pos)
    return square(TILESIZE) * matrix_number + matrix_pos


def get_pixel(letter, in_offset):
    """
    get the LED position for a given sign/character
    :type letter: Char
    :type in_offset: int (positive)
    :return: tupel of tupel, int
    """
    if ord(letter) < 128:  # if is ascii
        if letter.isalpha() and letter.isupper():
            r_tuple, r_offset = _get_pixel_from_ABC(letter)
        elif letter.isalpha() and letter.islower():
            r_tuple, r_offset = _get_pixel_from_abc(letter)
        elif letter.isdecimal():
            r_tuple, r_offset = _get_pixel_from_dec(letter)
        elif letter in "/\\ ?.!:;":
            r_tuple, r_offset = _get_pixel_from_special(letter)
        else:
            r_tuple = a.array("B", ())
            r_offset = 0
        return r_tuple, in_offset + r_offset


def _get_pixel_from_ABC(letter):
    """
    get the LED position for a given sign/character
    :type letter: Char
    :retval: tupel of tupel, int
    """
    if letter == "A":
        offset = 8
        print(offset)
        r_tuple = a.array("B", (0, 6, 1, 4, 1, 5, 1, 6, 2, 1,\
        2, 2, 2, 3, 3, 0, 3, 3, 4, 0, 4, 3, 5, 1, 5, 2, 5, 3, 5, 4, 5, 5, 5, 6, 6, 6))
    elif letter == "B":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 3, 3, 6, 4, 1, 4, 2, 4, 4, 4, 5))
    elif letter == "C":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5,\
        1, 0, 1, 1, 1, 5, 1, 6, 2, 0, 2, 6, 3, 0, 3, 6, 4, 1, 4, 5))
    elif letter == "D":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 0, 1, 6, 2, 0, 2, 6, 3, 1, 3, 5, 4, 2, 4, 3, 4, 4))
    elif letter == "E":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 6))
    elif letter == "F":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 0, 1, 3, 2, 0, 2, 3, 3, 0))
    elif letter == "G":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5,\
        1, 0, 1, 6, 2, 0, 2, 4, 2, 6, 3, 0, 3, 4, 3, 5, 4, 1, 4, 2, 4, 4, 4, 5, 4, 6))
    elif letter == "H":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 3, 2, 3, 3, 3, 4, 0, 4, 1, 4, 2, 4, 3, 4, 4, 4, 5, 4, 6))
    elif letter == "I":
        offset = 2
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6))
    elif letter == "J":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 5, 1, 0, 1, 6,\
        2, 0, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5))
    elif letter == "K":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 3, 2, 2, 2, 4, 3, 0, 3, 1, 3, 5, 3, 6))
    elif letter == "L":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 6, 2, 6, 3, 6))
    elif letter == "N":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 1, 1, 2, 2, 3, 2, 4, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "O":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5,\
        1, 0, 1, 1, 1, 5, 1, 6, 2, 0, 2, 6, 3, 0, 3, 1, 3, 5, 3, 6, 4, 1, 4, 2, 4, 3, 4, 4, 4, 5))
    elif letter == "P":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 0, 1, 3, 2, 0, 2, 3, 3, 0, 3, 3, 4, 1, 4, 2))
    elif letter == "Q":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5,\
        1, 0, 1, 1, 1, 5, 1, 6, 2, 0, 2, 4, 2, 6, 3, 0, 3, 1,\
        3, 5, 4, 1, 4, 2, 4, 3, 4, 4, 4, 6))
    elif letter == "R":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 1, 0, 1, 3, 2, 0, 2, 3, 2, 4, 2, 6, 3, 1, 3, 2, 3, 5, 3, 6))
    elif letter == "S":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 5, 1, 0, 1, 2,\
        1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 4, 3, 6, 4, 1, 4, 4, 4, 5))
    elif letter == "T":
        offset = 6
        r_tuple = a.array("B", (0, 0, 1, 0, 2, 0, 2, 1, 2, 2,\
        2, 3, 2, 4, 2, 5, 2, 6, 3, 0, 4, 0))
    elif letter == "U":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 1, 5, 1, 6, 2, 4, 2, 5, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "V":
        offset = 6
        r_tuple = a.array("B", (0, 0, 1, 0, 1, 1, 1, 2, 1, 3,\
        1, 4, 1, 5, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 4, 0))
    elif letter == "W":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        1, 4, 1, 5, 1, 6, 2, 0, 2, 1, 2, 3, 2, 4, 3, 0, 3, 4,\
        3, 5, 3, 6, 4, 0, 4, 1, 4, 2, 4, 3, 4, 4))
    elif letter == "X":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 6, 1, 1, 1, 2, 1, 4,\
        1, 5, 1, 0, 2, 3, 3, 1, 3, 2, 3, 4, 3, 5, 4, 5, 4, 6))
    elif letter == "Y":
        offset = 5
        r_tuple = a.array("B", (0, 0, 1, 1, 2, 2, 2, 3, 2, 4, 2, 5, 2, 6, 3, 0, 3, 1))
    elif letter == "Z":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 5, 0, 6, 1, 0, 1, 3,\
        1, 4, 2, 0, 2, 2, 2, 3, 2, 6, 3, 0, 3, 1, 3, 3, 3, 6, 4, 0, 4, 1, 4, 6))
    else:
        r_tuple = a.array("B", ())
        offset = 0
    return r_tuple, offset


def _get_pixel_from_dec(letter):
    """
    get the LED position for a given sign/character
    :type letter: Char
    :type in_offset: int (positive)
    :retval: tupel of tupel, int
    """
    if letter == "1":
        offset = 5
        r_tuple = a.array("B", (0, 2, 1, 1, 2, 0, 2, 1, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "2":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 6, 1, 0, 1, 5, 1, 6,\
        2, 0, 2, 5, 2, 6, 3, 0, 3, 3, 3, 4, 3, 6, 4, 1, 4, 2, 4, 6))
    elif letter == "3":
        offset = 7
        r_tuple = a.array("B", (0, 0, 0, 3, 0, 6, 1, 0, 1, 3,\
        1, 6, 2, 0, 2, 2, 2, 3, 2, 6, 3, 1, 3, 2, 3, 4, 3, 5))
    elif letter == "4":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 1, 4, 2, 4, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "5":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 5,\
        0, 6, 1, 0, 1, 4, 1, 6, 2, 0, 2, 4, 2, 5, 2, 6, 3, 0, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "6":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 1, 3, 4, 3, 5))
    elif letter == "7":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 3, 0, 5, 0, 6, 1, 0,\
        1, 3, 1, 4, 2, 0, 2, 1, 2, 2, 2, 3, 3, 0, 3, 1, 3, 3))
    elif letter == "8":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, \
        0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 3, 3, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "9":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 5,\
        0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "0":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 5,\
        0, 6, 1, 0, 1, 6, 2, 0, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    else:
        r_tuple = a.array("B", ())
        offset = 0
    return r_tuple, offset


def _get_pixel_from_special(letter):
    """
    get the LED position for a given sign/character
    :type letter: Char
    :retval: tupel of tupel, int
    """
    if letter == "/":
        offset = 4
        r_tuple = a.array("B", (0, 5, 0, 6, 1, 3, 1, 4, 1, 5, 2, 1, 2, 2, 2, 3, 3, 0, 3, 1))
    elif letter == '\\':
        offset = 4
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 6, 1, 1, 1, 2, 1, 3, 2, 3, 2, 4, 2, 4, 3, 5, 3, 6))
    elif letter == "?":
        offset = 4
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 3, 1, 0, 1, 2, 1, 4, 1, 6, 2, 0, 2, 1, 2, 3, 2, 4))
    elif letter == ".":
        offset = 2
        r_tuple = a.array("B", (0, 6))
    elif letter == "!":
        offset = 2
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 6))
    elif letter == ":":
        offset = 5
        r_tuple = a.array("B", (0, 3, 0, 5))
    elif letter == ",":
        offset = 2
        r_tuple = a.array("B", (0, 6, 0, 7, 1, 5, 0, 6))
    elif letter == ";":
        offset = 4
        r_tuple = a.array("B", (0, 6, 0, 7, 1, 5, 1, 6, 2, 3))
    else:
        r_tuple = a.array("B", ())
        offset = 0
    return r_tuple, offset


def _get_pixel_from_abc(letter):
    """
    get the LED position for a given sign/character
    :type letter: Char
    :retval: tupel of tupel, int
    """
    if letter == "a":
        offset = 6
        r_tuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 2, 3,\
        2, 6, 3, 4, 3, 5, 3, 6, 4, 3, 4, 4, 4, 5, 4, 6))
    elif letter == "b":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 4, 1, 6, 2, 3, 2, 6, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "c":
        offset = 4
        r_tuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 2, 3, 2, 6))
    elif letter == "d":
        offset = 5
        r_tuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 2, 4,\
        2, 5, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "e":
        offset = 5
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 1, 2, 1, 4,\
        1, 6, 2, 2, 2, 4, 2, 6, 3, 3, 3, 4, 3, 6))
    elif letter == "f":
        offset = 5
        r_tuple = a.array("B", (0, 3, 1, 0, 1, 1, 1, 2, 1, 4,\
        1, 5, 1, 6, 2, 0, 2, 3, 3, 0))
    elif letter == "g":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 7, 1, 3,\
        1, 5, 1, 7, 2, 3, 2, 4, 2, 5, 2, 6, 2, 7))
    elif letter == "h":
        offset = 4
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,\
        0, 5, 0, 6, 1, 3, 2, 3, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "i":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 3, 0, 4, 0, 5, 0, 6))
    elif letter == "j":
        offset = 5
        r_tuple = a.array("B", (0, 7, 0, 1, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7))
    elif letter == "k":
        offset = 4
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 5, 2, 3, 2, 4, 2, 6))
    elif letter == "l":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 1, 6))
    elif letter == "m":
        offset = 6
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 1, 4, 2,\
         4, 2, 5, 2, 6, 3, 4, 4, 4, 4, 5, 4, 6))
    elif letter == "n":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 1, 4, 2, 4, 2, 5, 2, 6))
    elif letter == "o":
        offset = 4
        r_tuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 2, 4, 2, 5))
    elif letter == "p":
        offset = 5
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 1, 3, 1, 5, 2, 3, 2, 5, 3, 4))
    elif letter == "q":
        offset = 6
        r_tuple = a.array("B", (0, 4, 1, 3, 1, 5, 2, 3, 2, 5, 3, 3, 3, 4, 3, 5, 3, 6, 3, 7))
    elif letter == "r":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 1, 4, 2, 3))
    elif letter == "s":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 6, 1, 3, 1, 4, 1, 5, 2, 3, 2, 5, 2, 6))
    elif letter == "t":
        offset = 4
        r_tuple = a.array("B", (0, 2, 1, 0, 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 2, 2))
    elif letter == "u":
        offset = 5
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 1, 6, 2, 5, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "v":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 1, 5, 1, 6, 2, 3, 2, 4))
    elif letter == "w":
        offset = 6
        r_tuple = a.array("B", (0, 3, 0, 4, 1, 5, 1, 6, 2, 4, 3, 5, 3, 6, 4, 3, 4, 4))
    elif letter == "x":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 1, 5, 1, 6, 3, 5, 3, 6, 4, 3, 4, 4))
    elif letter == "y":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 7, 1, 7, 2, 3, 2, 4, 2, 5, 2, 6, 2, 7))
    elif letter == "z":
        offset = 5
        r_tuple = a.array("B", (0, 3, 0, 6, 1, 3, 1, 5, 2, 3, 2, 4, 2, 6, 3, 3, 3, 6))
    else:
        r_tuple = a.array("B", ())
        offset = 0
    return r_tuple, offset


def restart(in_num=0):
    """
    Resetting the global offset value to inNum
    param inNum: int
    retval: none
    """
    global offset
    offset = in_num
    for index in range(0, NUMPIXELS):
        neopixels[index] = color_intensity(BLACK, 100.0)
        print(str(index) + " " + str(color_intensity(BLACK, 100.0)))
    neopixels.show()


def write(text, orientation="ZICZAC", color=WHITE, intensity=5):
    """
    Writes the param to the Neopixel Matrix
    param text: string
    retval: none
    """
    global offset
    for letter in text:
        pixels, next_offset = get_pixel(letter, offset)
        print(letter)
        print(pixels)
        write_raw(pixels, orientation, color, intensity)
        offset = next_offset


def write_raw(raw_position_list, orientation="ZICZAC", color=WHITE, intensity=5):
    """
    param raw_position_list: array (of bytes)
    param orientation: orientation of the matrices towards each other
    retval: none
    """
    global offset
    for index in range(0, len(raw_position_list), 2):
        x_pos = raw_position_list[index]
        y_pos = raw_position_list[index+1]
        pos = map_led(x_pos, y_pos, offset, orientation)
        gc.collect()
        if pos > NUMPIXELS-1:
            break
        elif pos < 0:
            continue
        else:
            print(pos)
            neopixels[pos] = color_intensity(color, intensity)
    neopixels.show()


if __name__ == "__main__":
    write("ABC")

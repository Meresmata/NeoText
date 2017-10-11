# writing texts with neopixels 8x8 matrices

from board import *
import adafruit_dotstar as dotstar
import time
import neopixel

offset = 0


def mapLed(position, orientation="Line"):
    tileSize = 8
    try:
        orientation.isalpha()
    finally:
        "orientation is not a string."

    orientation = orientation.upper()
    #if ((orientation != "LINE") | (orientation != "ZIPZAP")): throw("unknown orientation.")

    if (orientation == "LINE"):
        matrixpos = (offset + position(0)) % tileSize
        matrixnumber = (offset + position(0)) / tileSize
        return pow(tileSize, 2) * matrixnumber + (matrixpos) + tileSize * (position[1])


Alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890/?.!:; abcdefghijklmnopqrstuvwxyz".split()


def getPixel(Letter):
    global offset
    if Letter in Alphabet:
        if Letter == "A":
            offset += 7
            return (
            (0, 6), (1, 4), (1, 5), (1, 6), (2, 1), (2, 2), (2, 3), (3, 0), (3, 3), (4, 0), (4, 3), (5, 1), (5, 2),
            (5, 3), (5, 4), (5, 5), (5, 6), (6, 6))
        if Letter == "B":
            offset = 5
            return (
            (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 3), (1, 6), (2, 0), (2, 3), (2, 6),
            (3, 0), (3, 3), (3, 6), (4, 1), (4, 2), (4, 4), (4, 5))


#starting of the main programm
NUMPIXELS = 3*64
neopixels = neopixel.NeoPixel(D4, NUMPIXELS, brightness=0.1, auto_write=False)

WHITE = 0xffffff
RED = 0xff0000

for letter in "AB":
    pixels = getPixel(letter)

    for pixel in pixels:
        pos = mapLed(pixel)
        neopixels[pos] = 0xffffff
neopixels.show()


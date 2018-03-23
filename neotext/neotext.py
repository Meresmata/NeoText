"""
writing texts with up to 4  chained neopixel 8x8 matrices
author: Sebastian Heiden
"""

import gc
import array as a
import time

import board as b
import neopixel


class COLORS:
    """
    defining some colors for Type COLOR
    """
    WHITE = 0xffffff
    RED = 0xff0000
    BLUE = 0x0000ff
    YELLOW = 0xffff00
    CYAN = 0x00ffff
    MAGENTA = 0xff00ff
    ORANGE = 0xffa500
    GREEN = 0x00FF00
    BLACK = 0x000000


class Color:
    def __init__(self, color):
        if type(color) == tuple:
            int_color = color[0] << 16 | color[1] << 8 | color[2]
        else:
            int_color = color
        assert int_color >= 0
        assert int_color <= 0xFFFFFF

        self.color = int_color

    def to_int(self):
        return self.color

    def to_tuple(self):
        return self.color >> 16, (self.color & 0x00FF00) >> 8, (self.color & 0xFF)

    @staticmethod
    def intensity(color, percentage):
        """
        calculates the 24 bit color from a param
        color and param percentage (0.0 - 100.0)
        param color: int color code
        param percentage: float max percentage of led intensity
        return: int color code dimmed to max. percentage
        """
        assert type(color) == Color

        red = color.to_int() >> 16
        green = (color.to_int() & 0x00FF00) >> 8
        blue = color.to_int() & 0x0000FF

        red = int((red * percentage) / 100)
        green = int((green * percentage) / 100)
        blue = int((blue * percentage) / 100)

        return red, green, blue


def _square(base):
    """
    squares param base
    :type base: int base to be squared
    :return: int s
    """
    assert base > 0
    return int(pow(base, 2))


class NeoWrite:
    """
    class to Write text on up to four
    neopixel matrices
    """

    def __init__(self, num_tiles, pin, back_color=Color(COLORS.BLACK), intensity=5, orientation="ZIGZAG"):
        """
        :type num_tiles: int number of neopixel matrices
        :type pin: pin
        :type back_color: Color
        :type intensity: int
        """
        assert num_tiles <= 4
        assert num_tiles > 0
        assert intensity >= 0
        assert intensity <= 100
        assert orientation.upper() == "ZIGZAG" or orientation.upper() == "LINE"
        assert back_color.to_int() <= 0xFFFFFF
        assert back_color.to_int() >= 0

        self.offset = 0
        self.num_pixels = num_tiles * 64
        self.orientation = orientation.upper()
        self.neopixels = neopixel.NeoPixel(pin, self.num_pixels, auto_write=False)
        self.pixel_x_y_color = a.array("B", ())  # relay on sorting of pixels (upper left to lower right)
        self.element_byte_size = 5
        if back_color != Color(COLORS.BLACK):
            self.clear(0, back_color, intensity)
        self.time_stamp = time.monotonic()
        self.max_x = 0

    def _map_led(self, x_coord, y_coord):
        """
        map the position of the LED positions to the led numbers
        :type x_coord: int x-coordinate of LED
        :type y_coord: int y-coordinate of LED
        :return: int number of chained LED
        """
        # assert y_coord >= 0
        # assert y_coord < 8, str(y_coord) + " is to high."
        # assert x_coord >= 0
        # assert x_coord < self.num_pixels // 8

        tile_size = 8
        max_index = 7

        matrix_number = x_coord // tile_size

        if (self.orientation == "ZIGZAG") and (matrix_number % 2):
            matrix_pos = x_coord % tile_size + tile_size * y_coord
        else:
            matrix_pos = (max_index - y_coord) + tile_size * (x_coord % tile_size)

        return _square(tile_size) * matrix_number + matrix_pos

    def reset(self, in_num=0, back_color=Color(COLORS.BLACK), foreground_color=Color(COLORS.WHITE), intensity=5):
        """
        Resetting the global offset value to inNum, with back_color as color of the background
        foreground_color as color of the foreground and intensity as the overall max. intensity of each LED
        :type in_num: int selectable offset in x-position
        :type back_color: int color code
        :type foreground_color: int color code
        :type intensity: int max intensity of LED in percentage
        :return: None
        """
        assert in_num >= 0
        assert in_num < self.num_pixels // 8
        assert intensity >= 0
        assert intensity <= 100
        assert back_color <= 0xFFFFFF
        assert back_color >= 0
        assert foreground_color.to_int() <= 0xFFFFFF
        assert foreground_color.to_int() >= 0

        self.offset = in_num

        foreground_index = 0
        for index in range(0, self.num_pixels):
            # find out whether LED is in foreground or not
            next_foreground_led_num = self._map_led(self.pixel_x_y_color[foreground_index],
                                                    self.pixel_x_y_color[foreground_index + 1])
            if index < next_foreground_led_num:
                self.neopixels[index] = Color.intensity(back_color, intensity)
            elif index == next_foreground_led_num:
                self.neopixels[index] = Color.intensity(self.neopixels[foreground_index], intensity)
                foreground_index = foreground_index + self.element_byte_size
            # index should logically not be able to be be larger than compare value

        self.neopixels.show()

    def clear(self, in_num=0, back_color=Color(COLORS.BLACK), intensity=0):
        """
        clear to background color back_color with the max. intensity intensity
        and resetting the starting in_num for next write
        :type in_num: int number of x-position offset
        :type back_color: int color code to set
        :type intensity: int max. intensity of each led
        :return: None
        """
        assert in_num >= 0
        assert in_num < self.num_pixels // 8
        assert intensity >= 0
        assert intensity <= 100
        assert back_color.to_int() <= 0xFFFFFF
        assert back_color.to_int() >= 0

        self.offset = in_num

        for index in range(self.offset, self.num_pixels):
            self.neopixels[index] = Color.intensity(back_color, intensity)

        self.pixel_x_y_color = a.array("B", ())
        self.max_x = self.offset
        self.neopixels.show()

    def write(self, text, color=Color(COLORS.WHITE), intensity=5):
        """
        Writes the given text to the Neopixel Matrix with:
        :type text: string text to be written
        :type color: int color code for the LEDs
        :type intensity: int max. intensity for each LED
        :return: None
        """
        assert color.to_int() <= 0xFFFFFF
        assert color.to_int() >= 0
        assert intensity >= 0
        assert intensity <= 100

        for letter in text:
            pixels, next_offset = _get_pixel(letter, self.offset)
            self.write_raw(pixels, next_offset, color, intensity)

    def write_raw(self, raw_position_list, next_offset, color=Color(COLORS.WHITE), intensity=5):
        """
        Safe the raw (x,y)-Position in array of pixel positions
        :type raw_position_list: array (of Byte)
        :type next_offset: int, offset for placement of next letter
        :type color: int color code
        :type intensity: int max. intensity of each LED
        :return: None
        """
        assert intensity >= 0
        assert intensity <= 100
        assert color.to_int() <= 0xFFFFFF
        assert color.to_int() >= 0

        local_array = a.array("B", ())

        for index in range(0, len(raw_position_list), 2):
            # get x- and y-Position form array
            x_pos = raw_position_list[index]
            # if x_pos > self.max_x:
            #    self.max_x = x_pos
            if self.offset + x_pos + 2 > self.max_x:
                self.max_x = x_pos + self.offset + 2
            y_pos = raw_position_list[index + 1]

            # safe for redrawing
            self.pixel_x_y_color.append(x_pos + self.offset)
            local_array.append(x_pos + self.offset)
            self.pixel_x_y_color.append(y_pos)
            local_array.append(y_pos)

            # set color
            red, green, blue = Color.intensity(color, intensity)
            self.pixel_x_y_color.append(red)
            local_array.append(red)

            self.pixel_x_y_color.append(green)
            local_array.append(green)

            self.pixel_x_y_color.append(blue)
            local_array.append(blue)

        # "put" the result onto the LED MATRIX
        # self.put_pixels(self.pixel_xy_positions, color, intensity)
        self.__put_pixels(local_array)
        self.offset = next_offset

    def __put_pixels(self, in_array):
        """
        Write pixels into display takes relative positions of the displays into account
        :param in_array: array of bytes
        :return: None
        """
        for index in range(0, len(in_array), self.element_byte_size):
            # set each pixel, that fits into the display
            if in_array[index] < self.num_pixels//8:
                self.__put_pixel(in_array[index], in_array[index + 1], in_array[index + 2], in_array[index + 3],
                                 in_array[index + 4])

        self.neopixels.show()

    def __put_pixel(self, x_pos, y_pos, red, green, blue):
        """
        turn the LED of specified LED on, with the specified color
        :param x_pos: int from 0 to number of columns -1
        :param y_pos: int from 0 to number of rows -1
        :param red: int (byte)
        :param green: int (byte)
        :param blue: int (byte)
        :return: None
        """
        assert red <= 0xFF
        assert red >= 0
        assert green <= 0xFF
        assert green >= 0
        assert blue <= 0xFF
        assert blue >= 0
        assert x_pos < self.num_pixels//8  # number of total columns
        assert x_pos >= 0
        assert y_pos <= 8
        assert y_pos >= 0

        pos = self._map_led(x_pos, y_pos)
        gc.collect()
        if pos > self.num_pixels - 1:
            pass
        elif pos < 0:
            pass
        else:
            self.neopixels[pos] = (red, green, blue)

    def scroll(self, direction="LEFT", time_step=2.0):
        """
        Let the text run in top the left/right direction
        :param direction: str LEFT or RIGHT
        :param time_step: float time in ?(not specified in neopixel document, about a second?), current max 2 Hz
        :return: None
        """
        assert direction.upper() == "LEFT" or direction.upper() == "RIGHT"
        assert time_step > 0.0

        step = - 1 if direction.upper() == "LEFT" else +1

        furthest_right_pos = max(self.max_x, self.num_pixels//8)

        # calculate new positions, safe them locally, including their corresponding color
        if time.monotonic() >= self.time_stamp + time_step:
            # clear unused pixel
            for index in range(self.num_pixels):
                self.neopixels[index] = 0

            # for every position in use: x, y, red, green, blue
            for index in range(0, len(self.pixel_x_y_color), self.element_byte_size):
                x_pos = self.pixel_x_y_color[index]
                new_x_pos = (x_pos + step) % furthest_right_pos
                self.pixel_x_y_color[index] = new_x_pos

                if new_x_pos >= self.num_pixels // 8:
                    continue
                else:
                    # put used pixel
                    red = index + 2
                    green = index + 3
                    blue = index + 4

                    pos = self._map_led(new_x_pos, self.pixel_x_y_color[index + 1])
                    self.neopixels[pos] = (self.pixel_x_y_color[red], self.pixel_x_y_color[green],
                                           self.pixel_x_y_color[blue])

            self.neopixels.show()

    def deinit(self):
        self.neopixels.deinit()
        gc.collect()


def _get_pixel(character, in_offset):
    """
    get the LED position for a given sign/character
    :type character: String to write (extract each character and search for the resulting LED positions
    :type in_offset: int current x-position offset
    :return: byte array
    """
    assert len(character) == 1
    assert ord(character) < 128  # if is ascii

    if character.isalpha() and character.isupper():
        r_tuple, r_offset = _get_pixel_from_capitals(character)
    elif character.isalpha() and character.islower():
        r_tuple, r_offset = _get_pixel_from_minuscules(character)
    elif character.isdigit():
        r_tuple, r_offset = _get_pixel_from_dec(character)
    elif character in "/ ?.!:;, ":
        r_tuple, r_offset = _get_pixel_from_special(character)
    else:
        r_tuple = a.array("B", ())
        r_offset = 0
    return r_tuple, in_offset + r_offset


def _get_pixel_from_capitals(letter):
    """
    get the LED position for a given sign/character
    :type letter: string
    :return: byte array of int
    """
    if letter == "A":
        offset = 8
        r_tuple = a.array("B", (0, 6, 1, 4, 1, 5, 1, 6, 2, 1,
                                2, 2, 2, 3, 3, 0, 3, 3, 4, 0,
                                4, 3, 5, 1, 5, 2, 5, 3, 5, 4, 5, 5, 5, 6, 6, 6))
    elif letter == "B":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0,
                                3, 3, 3, 6, 4, 1, 4, 2, 4, 4, 4, 5))
    elif letter == "C":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5,
                                1, 0, 1, 1, 1, 5, 1, 6, 2, 0, 2, 6, 3, 0, 3, 6, 4, 1, 4, 5))
    elif letter == "D":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 0, 1, 6, 2, 0,
                                2, 6, 3, 1, 3, 5, 4, 2, 4, 3, 4, 4))
    elif letter == "E":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 0, 1, 3, 1, 6, 2, 0, 2, 3, 2, 6, 3, 0, 3, 6))
    elif letter == "F":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 0, 1, 3, 2, 0, 2, 3, 3, 0))
    elif letter == "G":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5,
                                1, 0, 1, 6, 2, 0, 2, 4, 2, 6,
                                3, 0, 3, 4, 3, 5, 4, 1, 4, 2,
                                4, 4, 4, 5, 4, 6))
    elif letter == "H":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 3, 2, 3, 3, 3,
                                4, 0, 4, 1, 4, 2, 4, 3, 4, 4, 4, 5, 4, 6))
    elif letter == "I":
        offset = 2
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6))
    elif letter == "J":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 5, 1, 0, 1, 6,
                                2, 0, 2, 6, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5))
    elif letter == "K":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 3, 2, 2, 2, 4, 3, 0, 3, 1, 3, 5, 3, 6))
    elif letter == "L":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 6, 2, 6, 3, 6))
    elif letter == "M":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 1, 1, 2, 2, 3,
                                3, 1, 3, 2, 4, 0, 4, 1, 4, 2,
                                4, 3, 4, 4, 4, 5, 4, 6))
    elif letter == "N":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 1, 1, 2, 2, 3,
                                2, 4, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "O":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5,
                                1, 0, 1, 1, 1, 5, 1, 6, 2, 0,
                                2, 6, 3, 0, 3, 1, 3, 5, 3, 6,
                                4, 1, 4, 2, 4, 3, 4, 4, 4, 5))
    elif letter == "P":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 0, 1, 3, 2, 0,
                                2, 3, 3, 0, 3, 3, 4, 1, 4, 2))
    elif letter == "Q":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 4, 0, 5,
                                1, 0, 1, 1, 1, 5, 1, 6, 2, 0,
                                2, 4, 2, 6, 3, 0, 3, 1, 3, 5,
                                4, 1, 4, 2, 4, 3, 4, 4, 4, 6))
    elif letter == "R":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 0, 1, 3, 2, 0,
                                2, 3, 2, 4, 3, 1, 3, 2, 3, 5, 3, 6))
    elif letter == "S":
        offset = 6
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 5, 1, 0, 1, 2,
                                1, 6, 2, 0, 2, 3, 2, 6, 3, 0,
                                3, 4, 3, 6, 4, 1, 4, 4, 4, 5))
    elif letter == "T":
        offset = 6
        r_tuple = a.array("B", (0, 0, 1, 0, 2, 0, 2, 1, 2, 2,
                                2, 3, 2, 4, 2, 5, 2, 6, 3, 0, 4, 0))
    elif letter == "U":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 1, 5, 1, 6, 2, 5, 3, 0,
                                3, 1, 3, 2, 3, 3, 3, 4, 3, 5,
                                3, 6))
    elif letter == "V":
        offset = 6
        r_tuple = a.array("B", (0, 0, 1, 0, 1, 1, 1, 2, 1, 3,
                                1, 4, 1, 5, 2, 6, 3, 0, 3, 1,
                                3, 2, 3, 3, 3, 4, 3, 5, 4, 0))
    elif letter == "W":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                1, 4, 1, 5, 1, 6, 2, 0, 2, 1,
                                2, 3, 2, 4, 3, 4, 3, 5, 3, 6,
                                4, 0, 4, 1, 4, 2, 4, 3, 4, 4))
    elif letter == "X":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 6, 1, 1, 1, 2, 1, 4,
                                1, 5, 1, 0, 2, 3, 3, 1, 3, 2,
                                3, 4, 3, 5, 4, 0, 4, 5, 4, 6))
    elif letter == "Y":
        offset = 5
        r_tuple = a.array("B", (0, 0, 1, 1, 2, 2, 2, 3, 2, 4,
                                2, 5, 2, 6, 3, 0, 3, 1))
    elif letter == "Z":
        offset = 6
        r_tuple = a.array("B", (0, 0, 0, 5, 0, 6, 1, 0, 1, 3,
                                1, 4, 2, 0, 2, 2, 2, 3, 2, 6,
                                3, 0, 3, 1, 3, 3, 3, 6, 4, 0, 4, 1, 4, 6))
    else:
        r_tuple = a.array("B", ())
        offset = 0
    return r_tuple, offset


def _get_pixel_from_dec(number):
    """
    get the LED positions for the given number
    :type number: string of the number 0-9
    :return: byte array
    """
    if number == "1":
        offset = 5
        r_tuple = a.array("B", (0, 2, 1, 1, 2, 0, 2, 1, 3, 0,
                                3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif number == "2":
        offset = 5
        r_tuple = a.array("B", (0, 1, 0, 6, 1, 0, 1, 4,
                                1, 5, 1, 6, 2, 0, 2, 3,
                                2, 6, 3, 1, 3, 2, 3, 4, 3, 6))
    elif number == "3":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 3, 0, 6, 1, 0, 1, 3,
                                1, 6, 2, 0, 2, 2, 2, 3, 2, 6,
                                3, 1, 3, 2, 3, 4, 3, 5))
    elif number == "4":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 1, 4,
                                2, 4, 3, 3, 3, 4, 3, 5, 3, 6))
    elif number == "5":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 5,
                                1, 0, 1, 3, 1, 6, 2, 0,
                                2, 3, 2, 6, 3, 0,
                                3, 4, 3, 5))
    elif number == "6":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 0, 1, 3, 1, 6,
                                2, 0, 2, 3, 2, 6, 3, 0, 3, 4, 3, 5))
    elif number == "7":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 3, 0, 5, 0, 6, 1, 0,
                                1, 3, 1, 4, 2, 0, 2, 1, 2, 2,
                                2, 3, 3, 0, 3, 1, 3, 3))
    elif number == "8":
        offset = 5
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 4, 0, 5, 1, 0,
                                1, 3, 1, 6, 2, 0, 2, 3, 2, 6,
                                3, 1, 3, 2, 3, 4, 3, 5))
    elif number == "9":
        offset = 5
        r_tuple = a.array("B", (0, 1, 0, 2, 0, 3, 0, 5, 0, 6,
                                1, 0, 1, 3, 1, 6, 2, 0, 2, 3,
                                2, 6, 3, 1, 3, 2, 3, 3, 3, 4,
                                3, 5))
    elif number == "0":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 0, 1, 6, 2, 0,
                                2, 6, 3, 0, 3, 1, 3, 2, 3, 3,
                                3, 4, 3, 5, 3, 6))
    else:
        r_tuple = a.array("B", ())
        offset = 0
    return r_tuple, offset


def _get_pixel_from_special(character):
    """
    get the LED position for a given sign/character
    :type character: string with one special character
    :return: byte array
    """
    if character == "/":
        offset = 4
        r_tuple = a.array("B", (0, 5, 0, 6, 1, 2, 1, 3, 1, 4,
                                1, 5, 2, 0, 2, 1, 2, 2))
    # elif character == '\\':
    #     offset = 4
    #    r_tuple = a.array("B", (0, 0, 0, 1, 0, 6, 1, 1, 1, 2,
    #                            1, 3, 2, 3, 2, 4, 2, 4, 3, 5, 3, 6))
    elif character == "?":
        offset = 4
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 3, 0, 4, 1, 0,
                                1, 2, 1, 4, 1, 6, 2, 0, 2, 1, 2, 4))
    elif character == ".":
        offset = 2
        r_tuple = a.array("B", (0, 6))
    elif character == "!":
        offset = 2
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 6))
    elif character == ":":
        offset = 2
        r_tuple = a.array("B", (0, 3, 0, 5))
    elif character == ",":
        offset = 2
        r_tuple = a.array("B", (0, 6, 0, 7, 1, 5, 0, 6))
    elif character == ";":
        offset = 2
        r_tuple = a.array("B", (0, 3, 0, 5, 0, 6, 0, 7))
    elif character == ",":
        offset = 2
        r_tuple = a.array("B", (0, 5, 0, 6, 0, 7))
    elif character == " ":
        offset = 1
        r_tuple = a.array("B", ())
    else:
        r_tuple = a.array("B", ())
        offset = 0
    return r_tuple, offset


def _get_pixel_from_minuscules(letter):
    """
        get the LED position for a given sign/character
        :type letter: string of one small cap. letter
        :return: byte array
        """
    if letter == "a":
        offset = 6
        r_tuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 2, 3,
                                2, 6, 3, 4, 3, 5, 4, 3, 4, 4, 4, 5, 4, 6))
    elif letter == "b":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 3, 1, 6, 2, 3,
                                2, 6, 3, 4, 3, 5))
    elif letter == "c":
        offset = 4
        r_tuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 2, 3, 2, 6))
    elif letter == "d":
        offset = 5
        r_tuple = a.array("B", (0, 4, 0, 5, 1, 3, 1, 6, 3, 0,
                                3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "e":
        offset = 5
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 1, 2, 1, 4,
                                1, 6, 2, 2, 2, 4, 2, 6, 3, 3, 3, 4, 3, 6))
    elif letter == "f":
        offset = 5
        r_tuple = a.array("B", (0, 3, 1, 0, 1, 1, 1, 2, 1, 3,
                                1, 4, 1, 5, 1, 6, 2, 0, 2, 3, 3, 0))
    elif letter == "g":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 7, 1, 3,
                                1, 5, 1, 7, 2, 3, 2, 4, 2, 5,
                                2, 6, 2, 7))
    elif letter == "h":
        offset = 5
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 3, 2, 3, 3, 3,
                                3, 4, 3, 5, 3, 6))
    elif letter == "i":
        offset = 2
        r_tuple = a.array("B", (0, 1, 0, 3, 0, 4, 0, 5, 0, 6))
    elif letter == "j":
        offset = 3
        r_tuple = a.array("B", (0, 7, 1, 1, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7))
    elif letter == "k":
        offset = 4
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                                0, 5, 0, 6, 1, 5, 2, 3, 2, 4, 2, 6))
    elif letter == "l":
        offset = 4
        r_tuple = a.array("B", (0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 1, 6, 2, 6))
    elif letter == "m":
        offset = 6
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 1, 4, 2,
                                4, 2, 5, 2, 6, 3, 4, 4, 4, 4, 5, 4, 6))
    elif letter == "n":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 1, 4, 2, 4, 2, 5, 2, 6))
    elif letter == "o":
        offset = 5
        r_tuple = a.array("B", (0, 4, 0, 5, 0, 6, 1, 3, 1, 6, 2, 3, 2, 6, 3, 4, 4, 5))
    elif letter == "p":
        offset = 5
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 1, 3, 1, 5, 2, 3, 2, 5, 3, 4))
    elif letter == "q":
        offset = 6
        r_tuple = a.array("B", (0, 4, 1, 3, 1, 5, 2, 3, 2, 5, 3, 3, 3, 4, 3, 5, 3, 6, 3, 7))
    elif letter == "r":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 6, 1, 4, 2, 3))
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
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 6, 1, 5, 2, 3, 2, 4, 2, 6))
    elif letter == "y":
        offset = 4
        r_tuple = a.array("B", (0, 3, 0, 4, 0, 5, 0, 7, 1, 5, 1, 7, 2, 3, 2, 4, 2, 5, 2, 6, 2, 7))
    elif letter == "z":
        offset = 5
        r_tuple = a.array("B", (0, 3, 0, 6, 1, 3, 1, 5, 1, 6, 2, 3, 2, 4, 2, 6, 3, 3, 3, 6))
    else:
        r_tuple = a.array("B", ())
        offset = 0
    return r_tuple, offset


def run_test():
    neo = NeoWrite(4, b.D4)
    neo.write("ABC")
    neo.write("DEF", color=Color(COLORS.BLUE))

    heart = a.array("B", (0, 3, 0, 4, 1, 2, 1, 3, 1, 4, 1, 5,
                          2, 3, 2, 4, 2, 5, 2, 6, 3, 4, 3, 5,
                          3, 6, 3, 7, 4, 3, 4, 4, 4, 5, 4, 6,
                          5, 2, 5, 3, 5, 4, 5, 5, 6, 3, 6, 4))
    neo.write_raw(heart, 8, Color(COLORS.RED))
    neo.scroll()

    large_number = 1 << 8
    time_interval = 0.1
    while large_number:
        neo.scroll(time_step=time_interval)
        large_number = large_number - 1

    neo.clear()
    neo.deinit()
    print("Test passed!")


if __name__ == "__main__":

    run_test()

"""
writing texts with up to 4  chained neopixel 8x8 matrices
author: Sebastian Heiden
"""

import digitalio
import gc
import time

import board as b
import neopixel_write


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


class NeoWrite:
    """
    class to Write text on up to four
    neopixel matrices
    """

    def __init__(self, num_tiles, pin, color=Color(COLORS.BLACK), intensity=5, orientation="ZIGZAG"):
        """
        :type num_tiles: int number of neopixel matrices
        :type pin: pin
        :type color: Color
        :type intensity: int
        """
        assert num_tiles <= 4
        assert num_tiles > 0
        assert intensity >= 0
        assert intensity <= 100
        assert orientation.upper() == "ZIGZAG" or orientation.upper() == "LINE"
        assert type(color) == Color
        assert color.to_int() <= 0xFFFFFF
        assert color.to_int() >= 0

        self.offset = 0
        self.num_pixels = num_tiles * 64
        self.orientation = 1 if orientation.upper() == "ZIGZAG" else 0
        self.pin = digitalio.DigitalInOut(pin)
        self.pixel_x_y_color = bytearray()  # relay on sorting of pixels (upper left to lower right)
        self.on_list = bytearray(self.num_pixels // 8)
        self.element_byte_size = 5
        self.background_color = color
        if color.to_int() != Color(COLORS.BLACK).to_int():
            self.clear(back_color=color, intensity=intensity)
        self.time_stamp = time.monotonic()
        self.max_x = 0
        self.max_x_y_index = 0

    def _map_led(self, x_coord, y_coord):
        """
        map the position of the LED positions to the led numbers
        :type x_coord: int x-coordinate of LED
        :type y_coord: int y-coordinate of LED
        :return: int number of chained LED
        """
        assert y_coord >= 0
        assert y_coord < 8, str(y_coord) + " is to high."
        assert x_coord >= 0
        assert x_coord < self.num_pixels // 8

        tile_size = 8
        max_index = 7

        matrix_number = x_coord // tile_size

        if self.orientation and (matrix_number % 2):
            matrix_pos = x_coord % tile_size + tile_size * y_coord
        else:
            matrix_pos = (max_index - y_coord) + tile_size * (x_coord % tile_size)

        return tile_size * tile_size * matrix_number + matrix_pos

    def _get_x_y(self, pos):
        num_rows = self.num_pixels // 8
        num_columns = 8
        if (pos // self.num_pixels) % 2 and self.orientation == 1:
            y_pos = pos % num_rows
            x_pos = (num_rows - 1) - pos // num_rows
        else:
            x_pos = pos // num_columns
            y_pos = pos % num_columns

        return x_pos, y_pos

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
        assert back_color.to_int() <= 0xFFFFFF
        assert back_color.to_int() >= 0
        assert foreground_color.to_int() <= 0xFFFFFF
        assert foreground_color.to_int() >= 0

        self.offset = in_num
        self.background_color = back_color

        for x in range(0, len(self.pixel_x_y_color), self.element_byte_size):
            self.pixel_x_y_color[2] = foreground_color.to_tuple()[0]
            self.pixel_x_y_color[3] = foreground_color.to_tuple()[1]
            self.pixel_x_y_color[4] = foreground_color.to_tuple()[2]

        self.show()

    def clear(self, back_color=Color(COLORS.BLACK), intensity=0):
        """
        clear to background color back_color with the max. intensity intensity
        and resetting the starting in_num for next write
        :type back_color: int color code to set
        :type intensity: int max. intensity of each led
        :return: None
        """
        assert intensity >= 0
        assert intensity <= 100
        assert back_color.to_int() <= 0xFFFFFF
        assert back_color.to_int() >= 0

        self.pixel_x_y_color = bytearray()
        self.on_list = bytearray(self.num_pixels // 8)  # clear on_list
        self.max_x = 0
        self.show(Color(Color.intensity(back_color, intensity)))

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
            print(letter)
            pixels, next_offset = _get_pixel(letter, self.offset)
            print(pixels)
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

        # clear all pixels
        for index in range(len(self.on_list)):
            self.on_list[index] = 0

        for index in range(0, len(raw_position_list), 2):
            # get x- and y-Position form array
            x_pos = raw_position_list[index]

            if self.offset + x_pos + 2 >= self.max_x:
                self.max_x = x_pos + self.offset + 2
                self.max_x_y_index = len(self.pixel_x_y_color) - 5  # get index of x-value of highest x,y Pos

            y_pos = raw_position_list[index + 1]

            # safe for redrawing
            self.pixel_x_y_color.append(x_pos + self.offset)
            self.pixel_x_y_color.append(y_pos)
            # set color
            red, green, blue = Color.intensity(color, intensity)
            self.pixel_x_y_color.append(red)
            self.pixel_x_y_color.append(green)
            self.pixel_x_y_color.append(blue)

            if(x_pos >= 0) and (x_pos <= self.num_pixels // 8):
                pos = self._map_led(x_pos, y_pos)
                self.set_on_list(pos)

        self.offset = next_offset
        self.show()

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

            self.on_list = bytearray(self.num_pixels // 8)

            # for every position in use: x, y, red, green, blue
            for index in range(0, len(self.pixel_x_y_color), self.element_byte_size):
                x_pos = self.pixel_x_y_color[index]
                new_x_pos = (x_pos + step) % furthest_right_pos
                # print(new_x_pos)
                self.pixel_x_y_color[index] = new_x_pos

                # set new correct self.max_x_y_index
                if new_x_pos + 1 >= self.max_x:
                    self.max_x = new_x_pos + 1
                    self.max_x_y_index = index

                if(new_x_pos >= 0) and (new_x_pos < self.num_pixels // 8):
                    pos = self._map_led(new_x_pos, self.pixel_x_y_color[index + 1])
                    self.set_on_list(pos)

            self.show()

    def set_on_list(self, pos):
        index = pos // 8
        byte = self.on_list[index]
        set_bit = byte | (1 << (7 - (pos % 8)))
        self.on_list[index] = set_bit
        return

    def get_color(self, index):

        get_red = lambda x_pos: self.pixel_x_y_color[x_pos + 2]
        get_green = lambda x_pos: self.pixel_x_y_color[x_pos + 3]
        get_blue = lambda x_pos: self.pixel_x_y_color[x_pos + 4]

        red, green, blue = 0, 0, 0

        x, y = self._get_x_y(index)

        # largest x at self.max_x_y_index, lowest at five entries further
        low_x_y_index = (self.max_x_y_index + 5) % len(self.pixel_x_y_color)

        # using heuristic for speed up, make a guess for index of x
        # guess ist ((4 * 5 x - 4/2 -1) + low_x_y_index) % len(matrix), 4 ~ estimated number of lines per x

        estimated_index = ((4 * x + 1) * self.element_byte_size + low_x_y_index) % len(self.pixel_x_y_color)

        if (self.pixel_x_y_color[estimated_index] <= x) and (self.pixel_x_y_color[estimated_index + 1] <= y):
                for index in range(estimated_index, len(self.pixel_x_y_color), self.element_byte_size):
                    if x == self.pixel_x_y_color[index]:
                        if y == self.pixel_x_y_color[index + 1]:
                            red = get_red(index)
                            green = get_green(index)
                            blue = get_blue(index)
                            break
        else:
            for index in range(estimated_index, low_x_y_index, - self.element_byte_size):
                if x == self.pixel_x_y_color[index]:
                    if y == self.pixel_x_y_color[index + 1]:
                        red = get_red(index)
                        green = get_green(index)
                        blue = get_blue(index)
                        break

        return red, green, blue

    def __get_on_list(self, item):
        row = self.on_list[item // 8]
        pixel = (row >> item % 8) & 1
        return pixel

    def show(self, back_color=Color(COLORS.BLACK)):

        byte_buf = bytearray(3 * self.num_pixels)  # zero
        for r1 in range(self.num_pixels):
            if self.__get_on_list(r1) == 1:
                buf = self.get_color(r1)
                for r2 in range(3):
                    byte_buf[3 * r1 + r2] = (buf[r2])

        neopixel_write.neopixel_write(self.pin, byte_buf)

    def deinit(self):
        self.reset()
        self.pin.deinit()
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
        r_tuple = bytearray()
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
        r_tuple = bytes((0, 6, 1, 4, 1, 5, 1, 6, 2, 1,
                        2, 2, 2, 3, 3, 0, 3, 3, 4, 0,
                        4, 3, 5, 1, 5, 2, 5, 3, 5, 4,
                        5, 5, 5, 6, 6, 6))
    elif letter == "B":
        offset = 6
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 0, 1, 3, 1, 6,
                        2, 0, 2, 3, 2, 6, 3, 0, 3, 3,
                        3, 6, 4, 1, 4, 2, 4, 4, 4, 5))
    elif letter == "C":
        offset = 6
        r_tuple = bytes((0, 1, 0, 2, 0, 3, 0, 4, 0, 5,
                        1, 0, 1, 1, 1, 5, 1, 6, 2, 0,
                        2, 6, 3, 0, 3, 6, 4, 1, 4, 5))

    elif letter == "D":
        offset = 6
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 0, 1, 6, 2, 0,
                        2, 6, 3, 1, 3, 5, 4, 2, 4, 3, 4, 4))
    elif letter == "E":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 0, 1, 3, 1, 6,
                        2, 0, 2, 3, 2, 6, 3, 0, 3, 6))
    elif letter == "F":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 0, 1, 3, 2, 0, 2, 3, 3, 0))
    elif letter == "G":
        offset = 6
        r_tuple = bytes((0, 1, 0, 2, 0, 3, 0, 4, 0, 5,
                        1, 0, 1, 6, 2, 0, 2, 4, 2, 6,
                        3, 0, 3, 4, 3, 5, 4, 1, 4, 2,
                        4, 4, 4, 5, 4, 6))
    elif letter == "H":
        offset = 6
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 3, 2, 3, 3, 3,
                        4, 0, 4, 1, 4, 2, 4, 3, 4, 4,
                        4, 5, 4, 6))
    elif letter == "I":
        offset = 2
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6))
    elif letter == "J":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 5, 1, 0, 1, 6,
                        2, 0, 2, 6, 3, 0, 3, 1, 3, 2,
                        3, 3, 3, 4, 3, 5))
    elif letter == "K":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 3, 2, 2, 2, 4,
                        3, 0, 3, 1, 3, 5, 3, 6))
    elif letter == "L":
        offset = 6
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                         0, 5, 0, 6, 1, 6, 2, 6, 3, 6))
    elif letter == "M":
        offset = 6
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 1, 1, 2, 2, 3,
                        3, 1, 3, 2, 4, 0, 4, 1, 4, 2,
                        4, 3, 4, 4, 4, 5, 4, 6))
    elif letter == "N":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 1, 1, 2, 2, 3,
                        2, 4, 3, 0, 3, 1, 3, 2, 3, 3,
                        3, 4, 3, 5, 3, 6))
    elif letter == "O":
        offset = 6
        r_tuple = bytes((0, 1, 0, 2, 0, 3, 0, 4, 0, 5,
                        1, 0, 1, 1, 1, 5, 1, 6, 2, 0,
                        2, 6, 3, 0, 3, 1, 3, 5, 3, 6,
                        4, 1, 4, 2, 4, 3, 4, 4, 4, 5))
    elif letter == "P":
        offset = 6
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 0, 1, 3, 2, 0,
                        2, 3, 3, 0, 3, 3, 4, 1, 4, 2))
    elif letter == "Q":
        offset = 6
        r_tuple = bytes((0, 1, 0, 2, 0, 3, 0, 4, 0, 5,
                        1, 0, 1, 1, 1, 5, 1, 6, 2, 0,
                        2, 4, 2, 6, 3, 0, 3, 1, 3, 5,
                        4, 1, 4, 2, 4, 3, 4, 4, 4, 6))
    elif letter == "R":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 0, 1, 3, 2, 0,
                        2, 3, 2, 4, 3, 1, 3, 2, 3, 5, 3, 6))
    elif letter == "S":
        offset = 6
        r_tuple = bytes((0, 1, 0, 2, 0, 5, 1, 0, 1, 2,
                        1, 6, 2, 0, 2, 3, 2, 6, 3, 0,
                        3, 4, 3, 6, 4, 1, 4, 4, 4, 5))
    elif letter == "T":
        offset = 6
        r_tuple = bytes((0, 0, 1, 0, 2, 0, 2, 1, 2, 2,
                         2, 3, 2, 4, 2, 5, 2, 6, 3, 0, 4, 0))
    elif letter == "U":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 1, 5, 1, 6, 2, 5, 3, 0,
                        3, 1, 3, 2, 3, 3, 3, 4, 3, 5,
                        3, 6))
    elif letter == "V":
        offset = 6
        r_tuple = bytes((0, 0, 1, 0, 1, 1, 1, 2, 1, 3,
                        1, 4, 1, 5, 2, 6, 3, 0, 3, 1,
                        3, 2, 3, 3, 3, 4, 3, 5, 4, 0))
    elif letter == "W":
        offset = 6
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        1, 4, 1, 5, 1, 6, 2, 0, 2, 1,
                        2, 3, 2, 4, 3, 4, 3, 5, 3, 6,
                        4, 0, 4, 1, 4, 2, 4, 3, 4, 4))
    elif letter == "X":
        offset = 5
        r_tuple = bytes((0, 0, 0, 6, 1, 1, 1, 2, 1, 4,
                        1, 5, 1, 0, 2, 3, 3, 1, 3, 2,
                        3, 4, 3, 5, 4, 0, 4, 5, 4, 6))
    elif letter == "Y":
        offset = 5
        r_tuple = bytes((0, 0, 1, 1, 2, 2, 2, 3, 2, 4,
                        2, 5, 2, 6, 3, 0, 3, 1))
    elif letter == "Z":
        offset = 6
        r_tuple = bytes((0, 0, 0, 5, 0, 6, 1, 0, 1, 3,
                        1, 4, 2, 0, 2, 2, 2, 3, 2, 6,
                        3, 0, 3, 1, 3, 3, 3, 6, 4, 0,
                        4, 1, 4, 6))
    else:
        r_tuple = bytes(())
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
        r_tuple = bytes((0, 2, 1, 1, 2, 0, 2, 1, 3, 0,
                        3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif number == "2":
        offset = 5
        r_tuple = bytes((0, 1, 0, 6, 1, 0, 1, 4,
                        1, 5, 1, 6, 2, 0, 2, 3,
                        2, 6, 3, 1, 3, 2, 3, 4, 3, 6))
    elif number == "3":
        offset = 5
        r_tuple = bytes((0, 0, 0, 3, 0, 6, 1, 0, 1, 3,
                        1, 6, 2, 0, 2, 2, 2, 3, 2, 6,
                        3, 1, 3, 2, 3, 4, 3, 5))
    elif number == "4":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 1, 4,
                        2, 4, 3, 3, 3, 4, 3, 5, 3, 6))
    elif number == "5":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 5,
                        1, 0, 1, 3, 1, 6, 2, 0,
                        2, 3, 2, 6, 3, 0,
                        3, 4, 3, 5))
    elif number == "6":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 0, 1, 3, 1, 6,
                        2, 0, 2, 3, 2, 6, 3, 0, 3, 4, 3, 5))
    elif number == "7":
        offset = 5
        r_tuple = bytes((0, 0, 0, 3, 0, 5, 0, 6, 1, 0,
                        1, 3, 1, 4, 2, 0, 2, 1, 2, 2,
                        2, 3, 3, 0, 3, 1, 3, 3))
    elif number == "8":
        offset = 5
        r_tuple = bytes((0, 1, 0, 2, 0, 4, 0, 5, 1, 0,
                        1, 3, 1, 6, 2, 0, 2, 3, 2, 6,
                        3, 1, 3, 2, 3, 4, 3, 5))
    elif number == "9":
        offset = 5
        r_tuple = bytes((0, 1, 0, 2, 0, 3, 0, 5, 0, 6,
                        1, 0, 1, 3, 1, 6, 2, 0, 2, 3,
                        2, 6, 3, 1, 3, 2, 3, 3, 3, 4,
                        3, 5))
    elif number == "0":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 0, 1, 6, 2, 0,
                        2, 6, 3, 0, 3, 1, 3, 2, 3, 3,
                        3, 4, 3, 5, 3, 6))
    else:
        r_tuple = bytes()
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
        r_tuple = bytes((0, 5, 0, 6, 1, 2, 1, 3, 1, 4,
                        1, 5, 2, 0, 2, 1, 2, 2))
    # elif character == '\\':
    #     offset = 4
    #    r_tuple = bytes((0, 0, 0, 1, 0, 6, 1, 1, 1, 2,
    #                            1, 3, 2, 3, 2, 4, 2, 4, 3, 5, 3, 6))
    elif character == "?":
        offset = 4
        r_tuple = bytes((0, 0, 0, 1, 0, 3, 0, 4, 1, 0,
                        1, 2, 1, 4, 1, 6, 2, 0, 2, 1, 2, 4))
    elif character == ".":
        offset = 2
        r_tuple = bytes((0, 6))
    elif character == "!":
        offset = 2
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 6))
    elif character == ":":
        offset = 2
        r_tuple = bytes((0, 3, 0, 5))
    elif character == ",":
        offset = 2
        r_tuple = bytes((0, 6, 0, 7, 1, 5, 0, 6))
    elif character == ";":
        offset = 2
        r_tuple = bytes((0, 3, 0, 5, 0, 6, 0, 7))
    elif character == ",":
        offset = 2
        r_tuple = bytes((0, 5, 0, 6, 0, 7))
    elif character == " ":
        offset = 1
        r_tuple = bytes(())
    else:
        r_tuple = bytes(())
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
        r_tuple = bytes((0, 4, 0, 5, 1, 3, 1, 6, 2, 3,
                        2, 6, 3, 4, 3, 5, 4, 3, 4, 4,
                        4, 5, 4, 6))
    elif letter == "b":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                         0, 5, 0, 6, 1, 3, 1, 6, 2, 3,
                         2, 6, 3, 4, 3, 5))
    elif letter == "c":
        offset = 4
        r_tuple = bytes((0, 4, 0, 5, 1, 3, 1, 6, 2, 3, 2, 6))
    elif letter == "d":
        offset = 5
        r_tuple = bytes((0, 4, 0, 5, 1, 3, 1, 6, 3, 0,
                        3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "e":
        offset = 5
        r_tuple = bytes((0, 3, 0, 4, 0, 5, 1, 2, 1, 4,
                        1, 6, 2, 2, 2, 4, 2, 6, 3, 3, 3, 4, 3, 6))
    elif letter == "f":
        offset = 5
        r_tuple = bytes((0, 3, 1, 0, 1, 1, 1, 2, 1, 3,
                        1, 4, 1, 5, 1, 6, 2, 0, 2, 3, 3, 0))
    elif letter == "g":
        offset = 4
        r_tuple = bytes((0, 3, 0, 4, 0, 5, 0, 7, 1, 3,
                        1, 5, 1, 7, 2, 3, 2, 4, 2, 5,
                        2, 6, 2, 7))
    elif letter == "h":
        offset = 5
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 3, 2, 3, 3, 3,
                        3, 4, 3, 5, 3, 6))
    elif letter == "i":
        offset = 2
        r_tuple = bytes((0, 1, 0, 3, 0, 4, 0, 5, 0, 6))
    elif letter == "j":
        offset = 3
        r_tuple = bytes((0, 7, 1, 1, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7))
    elif letter == "k":
        offset = 4
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                        0, 5, 0, 6, 1, 5, 2, 3, 2, 4, 2, 6))
    elif letter == "l":
        offset = 4
        r_tuple = bytes((0, 0, 0, 1, 0, 2, 0, 3, 0, 4,
                         0, 5, 1, 6, 2, 6))
    elif letter == "m":
        offset = 6
        r_tuple = bytes((0, 3, 0, 4, 0, 5, 0, 6, 1, 4,
                         2, 4, 2, 5, 2, 6, 3, 4, 4, 4,
                         4, 5, 4, 6))
    elif letter == "n":
        offset = 4
        r_tuple = bytes((0, 3, 0, 4, 0, 5, 0, 6, 1, 4, 2, 4, 2, 5, 2, 6))
    elif letter == "o":
        offset = 5
        r_tuple = bytes((0, 4, 0, 5, 0, 6, 1, 3, 1, 6, 2, 3, 2, 6, 3, 4, 4, 5))
    elif letter == "p":
        offset = 5
        r_tuple = bytes((0, 3, 0, 4, 0, 5, 0, 6, 1, 3, 1, 5, 2, 3, 2, 5, 3, 4))
    elif letter == "q":
        offset = 6
        r_tuple = bytes((0, 4, 1, 3, 1, 5, 2, 3, 2, 5, 3, 3, 3, 4, 3, 5, 3, 6, 3, 7))
    elif letter == "r":
        offset = 4
        r_tuple = bytes((0, 3, 0, 4, 0, 5, 0, 6, 1, 4, 2, 3))
    elif letter == "s":
        offset = 4
        r_tuple = bytes((0, 3, 0, 4, 0, 6, 1, 3, 1, 4, 1, 5, 2, 3, 2, 5, 2, 6))
    elif letter == "t":
        offset = 4
        r_tuple = bytes((0, 2, 1, 0, 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 2, 2))
    elif letter == "u":
        offset = 5
        r_tuple = bytes((0, 3, 0, 4, 0, 5, 1, 6, 2, 5, 3, 3, 3, 4, 3, 5, 3, 6))
    elif letter == "v":
        offset = 4
        r_tuple = bytes((0, 3, 0, 4, 1, 5, 1, 6, 2, 3, 2, 4))
    elif letter == "w":
        offset = 6
        r_tuple = bytes((0, 3, 0, 4, 1, 5, 1, 6, 2, 4, 3, 5, 3, 6, 4, 3, 4, 4))
    elif letter == "x":
        offset = 4
        r_tuple = bytes((0, 3, 0, 4, 0, 6, 1, 5, 2, 3, 2, 4, 2, 6))
    elif letter == "y":
        offset = 4
        r_tuple = bytes((0, 3, 0, 4, 0, 5, 0, 7, 1, 5, 1, 7, 2, 3, 2, 4, 2, 5, 2, 6, 2, 7))
    elif letter == "z":
        offset = 5
        r_tuple = bytes((0, 3, 0, 6, 1, 3, 1, 5, 1, 6, 2, 3, 2, 4, 2, 6, 3, 3, 3, 6))
    else:
        r_tuple = bytes(())
        offset = 0
    return r_tuple, offset


def run_test():
    neo = NeoWrite(4, b.D4, orientation="LINE")
    # neo.write("i")
    neo.write("Wanna ")
    neo.write("marry", color=Color(COLORS.BLUE))
    neo.write(" me? ")

    heart = bytes((0, 3, 0, 4, 1, 2, 1, 3, 1, 4, 1, 5,
                  2, 3, 2, 4, 2, 5, 2, 6, 3, 4, 3, 5,
                  3, 6, 3, 7, 4, 3, 4, 4, 4, 5, 4, 6,
                  5, 2, 5, 3, 5, 4, 5, 5, 6, 3, 6, 4))
    neo.write_raw(heart, 8, Color(COLORS.RED))
    neo.scroll()

    large_number = 1 << 8
    time_interval = 0.1
    while large_number:
        current_time = time.monotonic()
        if current_time >= neo.time_stamp + time_interval:
            neo.scroll(time_step=time_interval)
            large_number = large_number - 1

    neo.clear()
    neo.deinit()
    print("Test passed!")


if __name__ == "__main__":

    run_test()

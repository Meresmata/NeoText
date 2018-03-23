# NeoText

This is a module for Circuit python. It uses the neopixel module to draw text and signs onto neopixel matrices. The model
can deal with 4 matrices. (Neopixels limit of 256 pixels in a row)

Assumption: the displays lie next to each other in one line. The relative orientations may be:
all with their first pixel in the lower left corner, or alternating: with the first and the third matrix with the first
pixel in the lower left corner and the second and forth matrices with their first pixel in the upper left corner.
The later alternative needs shorter cables.

**Usage:**

Initialization:
The class needs follow informations:

Number of matrices in a row (up to four).
Pin, controlling the matrices.

Optionally: 

Default color of the background, defaults to black.
Intensity of the pixels in percent, defaults to 5 %.
Relative orientation of the matrices, defaults to "ZIGZAG".

To write pixels on the matrices you can use the method _write_ or _write_raw_. The former uses strings of letter, numbers
and some special characters, the later uses only an array of x, y coordinates. X = 0, Y = 0. is the first pixel of the
first matrix. Higher X--> more the the right, higher y--> more to the top.

Options are: characters color and intensity for the given string or x,y coordinate.

Additionally the text can be scrolled right or left with _scroll_. 
Optional parameters: 
Direction defaults to left.
time, defaults to one column per 2 s.
The scrolling is somewhat limited up to now. The current maximum speed is about 2 columns per second. (time = 0.5) 


**Example:**

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

   
 Comment on the array heart. Using byte array safes ram. Two elements make up one pixel. The x-Coordinate is the first
 element, the y_Coordinate the later. For Example: the first pixel of the heart is pixel (0, 3), followed by pixel
 (0, 4)...
 
 I am looking forward for your suggestions especially about improving the scrolling speed, code size and usability. 
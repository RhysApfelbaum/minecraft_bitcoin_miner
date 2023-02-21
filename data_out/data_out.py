from PIL import Image
import os
from config import *

# Find the most recent screenshot in screenshots folder
screenshots = os.listdir(SCREENSHOT_PATH)
img_path = os.path.join(SCREENSHOT_PATH, screenshots[0])

for i in screenshots:
    candidate_path = os.path.join(SCREENSHOT_PATH, i)
    if os.path.getmtime(candidate_path) > os.path.getmtime(img_path):
        img_path = candidate_path

# Get the rounded greyscale colour at coord (x, y)
def get_pix_val(im, coord):
    pixel = im.getpixel(coord)
    return round((pixel[0] + pixel[1] + pixel[2]) / (255 * 3))

# Format 32 bit int as hex
def prettyhex32(a):
    raw = '{:08x}'.format(a)
    result = ''
    for i in range(0, 8, 2):
        result += raw[i] + raw[i + 1] + ' '
    return result

with Image.open(img_path) as im:
    x_squares = []
    y_squares = []

    # Use the guide pixels to find the x and y coordinates
    guide = STARTING_PIXEL[1]
    last_val = get_pix_val(im, (STARTING_PIXEL[0], STARTING_PIXEL[1]))
    while len(y_squares) < NUM_Y_SQUARES:
        if get_pix_val(im, (STARTING_PIXEL[0], guide)) != last_val:
            y_squares.append(guide)
            last_val = 1 - last_val
        guide -= 1
    
    last_val = get_pix_val(im, (STARTING_PIXEL[0], STARTING_PIXEL[1]))
    guide = STARTING_PIXEL[0]
    while len(x_squares) < NUM_X_SQUARES:
        if get_pix_val(im, (guide, STARTING_PIXEL[1])) != last_val:
            x_squares.append(guide)
            last_val = 1 - last_val
        guide -= 1

    # convert each pixel column to an integer
    # TODO: this should probably be a bytearray, but keeping it as int now is a bit easier
    hnum_label = 0
    for i in range(0, NUM_X_SQUARES, 2):
        mask = 0x80000000
        word = 0
        x = x_squares[i]
        for y in y_squares:
            word += mask * get_pix_val(im, (x, y))
            mask >>= 1
        
        print('h%d: %s' % (hnum_label, prettyhex32(word)))
        hnum_label += 1


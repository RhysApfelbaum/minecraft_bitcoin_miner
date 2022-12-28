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


# input(img_path)

def get_pix_val(im, coord):
    pixel = im.getpixel(coord)
    return round((pixel[0] + pixel[1] + pixel[2]) / (255 * 3))

# format 32 bit int as hex
def prettyhex32(a):
    raw = '{:08x}'.format(a)
    result = ''
    for i in range(0, 8, 2):
        result += raw[i] + raw[i + 1] + ' '
    return result


with Image.open(img_path) as im:
    # track each map pixel location using starting values in config.py
    x_values = [STARTING_PIXEL[0]]
    y_values = [STARTING_PIXEL[1]]

    
    y_guide = Y_INIT
    last_val = get_pix_val(im, (X_GUIDE, Y_INIT))
    while len(y_values) < 32:
        if get_pix_val(im, (X_GUIDE, y_guide)) != last_val:
            y_values.append(y_guide)
            last_val = 1 - last_val
        y_guide -= 1

    # convert each pixel column to an integer
    # TODO: this should probably be a bytearray, but keeping it as int now is a bit easier
    labels = 'abcdefgh'
    labelx = 0
    for x in X_VALS:
        mask = 0x80000000
        word = 0
        for y in y_values:
            word += mask * get_pix_val(im, (x, y))
            mask >>= 1
        
        print('%s: %s' % (labels[labelx], prettyhex32(word)))
        labelx += 1
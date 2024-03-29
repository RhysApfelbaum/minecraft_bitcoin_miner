from PIL import Image
import os
import json

config_path = os.path.join(
    os.path.dirname(__file__),
    'config.json'
)
with open(config_path, 'r') as fp:
    config = json.load(fp)
start_x = config['starting_pixel_x'] 
start_y = config['starting_pixel_y'] 

# Find the most recent screenshot in screenshots folder
screenshots = os.listdir(config['screenshots_path'])
img_path = os.path.join(config['screenshots_path'], screenshots[0])

for i in screenshots:
    candidate_path = os.path.join(config['screenshots_path'], i)
    if os.path.getmtime(candidate_path) > os.path.getmtime(img_path):
        img_path = candidate_path

# Get the rounded greyscale colour at coord (x, y)
def get_pix_val(im, coord):
    pixel = im.getpixel(coord)
    return round(((pixel[0] + pixel[1] + pixel[2]) + 0) / (255 * 3))

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
    guide = start_y
    last_val = get_pix_val(im, (start_x, start_y))
    while len(y_squares) < config['num_y_squares']:
        if get_pix_val(im, (start_x, guide)) != last_val:
            y_squares.append(guide)
            last_val = 1 - last_val
        guide -= 1
    
    last_val = get_pix_val(im, (start_x, start_y))
    guide = start_x 
    while len(x_squares) < config['num_x_squares']:
        if get_pix_val(im, (guide, start_y)) != last_val:
            x_squares.append(guide)
            last_val = 1 - last_val
        guide += 1

    # convert each pixel column to an integer
    # TODO: this should probably be a bytearray, but keeping it as int now is a bit easier
    hnum_label = 0
    for i in range(0, config['num_x_squares'], 2):
        mask = 0x80000000
        word = 0
        x = x_squares[i]
        for y in y_squares:
            word += mask * get_pix_val(im, (x, y))
            mask >>= 1
        print('%s: %s' % ('abcdefgh'[hnum_label] ,prettyhex32(word)))
        hnum_label += 1
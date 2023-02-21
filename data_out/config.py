SCREENSHOT_PATH = r'C:\Users\rhysl\.minecraft-installations\fabric\screenshots'

# These values depend on where we put the data out blocks and where the map is on the screen, so they're almost definitely wrong.
# This is based on there being 1 guide line with alternating black and white pixels, and 8 output lines with the a-h.
# Turns out the outputs are not quite a-h, a-h plus whatever value is in our eight output registers, starting with the init values.
# This is a line I'm trying to write here.

STARTING_PIXEL = [422, 751] # This is the red block on the map. It rounds to 0 (black), so it should be followed by a white block.
NUM_X_SQUARES = 15
NUM_Y_SQUARES = 32


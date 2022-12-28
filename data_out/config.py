SCREENSHOT_PATH = r'C:\Users\rhysl\.minecraft-installations\fabric\screenshots'

# These values depend on where we put the data out blocks and where the map is on the screen, so they're almost definitely wrong.
# This is based on there being 1 guide line with alternating black and white pixels, and 8 output lines with the a-h.
# Turns out the outputs are not quite a-h, a-h plus whatever value is in our eight output registers, starting with the init values.

STARTING_PIXEL = [0, 0]
X_VALS = [1068, 1012, 987, 962, 882, 826, 801, 782] # x coords inside the first pixel of each output line. the y coords are generated from the guide line
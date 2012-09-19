#!/usr/bin/env python

from PIL import Image, ImageDraw
import sys
import re
import os

sx = 512


files = os.listdir("pictures")

x1 = 0
y1 = 0

x2 = 0
y2 = 0

for file in files:
    z = list(re.search("(\d+)(\w)(\d+)(\w)", file).groups())

    if z[1] == 'n':
        y1 = max(y1, int(z[0]))
    else:
        y2 = max(y2, int(z[0]))

    if z[3] == 'w':
        x1 = max(x1, int(z[2]))
    else:
        x2 = max(x2, int(z[2]))


size_x = (x1 + x2) * sx
size_y = (y1 + y2) * sx

print size_x, size_y

im = Image.open("pictures/" + files[0])

img = Image.new(im.mode, (size_x, size_y), 255)
draw = ImageDraw.Draw(img)
#draw.rectangle([(0, sx * x1), (size_x, size_y)], fill="black", outline="black")
#draw.rectangle((1, 10, 90, 90), fill="black", outline="black")
draw.rectangle([(1, sx * y1), (size_x, size_y)], fill="black", outline="black")

for file in files:
    print file
    z = list(re.search("(\d+)(\w)(\d+)(\w)", file).groups())

    coord_y = 0

    if z[3] == 'w':
        coord_x = (x1 - int(z[2])) * sx
    else:
        coord_x = sx * int(z[2]) + (sx * (x1 - 1))

    if z[1] == 'n':
        coord_y = (y1 - int(z[0])) * sx
    else:
        coord_y = sx * int(z[0]) + (sx * (y1 - 1))

    print coord_x, coord_y
    img.paste(Image.open("pictures/" + file), (coord_x, coord_y))

img.save("full.png")


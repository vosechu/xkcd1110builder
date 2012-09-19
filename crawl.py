#!/usr/bin/env python

import os.path
import sys
import urllib2
import re

points_fd = open("points.valid")
valid_points = points_fd.read().split()
points_fd.close()

points_fd = open("points.invalid")
invalid_points = points_fd.read().split()
points_fd.close()

def get_brothers(point, rec_level):

    if rec_level == -1:
        return []

    brothers = []
    z = list(re.search("(\d+)(\w)(\d+)(\w)", point).groups())

    brothers.append(''.join([str(int(z[0]) + 1)] + z[1:]))
    brothers.append(''.join(z[0:2] + [str(int(z[2]) + 1)] + z[3:]))

    x1 = z[0]; x2 = z[1]
    x1 = int(x1) - 1
    if x1 == 0:
        x1 = 1
        if x2 == 'n':
            x2 = 's'
        else:
            x2 = 'n'

    brothers.append(''.join([str(x1), x2] + z[2:]))

    y1 = z[2]; y2 = z[3]
    y1 = int(y1) - 1
    if y1 == 0:
        y1 = 1
        if y2 == 'w':
            y2 = 'e'
        else:
            y2 = 'w'

    brothers.append(''.join(z[:2] + [str(y1), y2]))

    sub_brothers = []

    for brother in brothers:
        sub_brothers = sub_brothers + get_brothers(brother, rec_level - 1)

    return brothers + sub_brothers

while len(valid_points) > 0:
    # check that pictures/<point>.png does not exist.

    point = valid_points[0]

    print "Trying point: %s" % point

    picture_file_name = "pictures.full/" + point + ".png"

    if os.path.isfile(picture_file_name):
        valid_points.remove(point)
        continue

    # crawling picture

    url = "http://imgs.xkcd.com/clickdrag/%s.png" % point

    try:
        picture_urlobj = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        print e
        valid_points.remove(point)
        invalid_points.append(point)
        continue

    if picture_urlobj.getcode() == 200:
        # Save pictures
        fd = open(picture_file_name, "w")
        fd.write(picture_urlobj.read())
        fd.close()

        # point is valid: adding brothers in valid_points.
        brothers = get_brothers(point, 6)

        for brother in brothers:
            if brother not in valid_points and brother not in invalid_points:
                valid_points.append(brother)

        # Remove point from valid_points.
        valid_points.remove(point)

    # backup files
    points_fd = open("points.valid", "w")
    points_fd.write('\n'.join(valid_points))
    points_fd.close()

    points_fd = open("points.invalid", "w")
    points_fd.write('\n'.join(invalid_points))
    points_fd.close()
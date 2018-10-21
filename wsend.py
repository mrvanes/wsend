#!/usr/bin/python
import threading

import utils
import patterns

threading.Timer(1, utils.getkey).start()

color = 0.5
speed = 0.5
utils.KEY = ptrn = '1'

while 1:
    if utils.KEY == 'q':
        print('')
        break
    elif utils.KEY == '[':
        color -= 0.1
    elif utils.KEY == ']':
        color += 0.1
    elif utils.KEY == '{':
        speed *= 1.5
    elif utils.KEY == '}':
        speed /= 1.5
    else:
        ptrn = utils.KEY
    utils.KEY = ptrn
    if color < 0:
        color += 1
    if color > 1:
        color -= 1

    speed = max(0.1, speed)
    patterns.pattern(ptrn, speed, color)


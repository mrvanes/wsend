#!/usr/bin/python
import colorsys
import termios
import sys
import tty

KEY = ''

def hsv2rgb(h, s, v):
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def getkey():
    global KEY
    settings = termios.tcgetattr(sys.stdin)
    tty.setraw(sys.stdin)
    while True:
        KEY = sys.stdin.read(1)
        #sys.stdout.write(KEY)
        #sys.stdout.flush()
        if KEY == 'q':
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
            break

def next_time(t0, dt):
    while 1:
        t0 += dt
        yield t0


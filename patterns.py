#!/usr/bin/python
import socket
import utils
import time
import random

#UDP_IP = "192.168.42.10"
UDP_IP = "192.168.42.255"
UDP_PORT = 7777
LENGTH = 4
FPS = 25

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sckt.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sckt.connect((UDP_IP, UDP_PORT))

def pattern(pattern, color, speed):
    global sckt, LENGTH, FPS, TIMER
    print("P: %s, c: %.1f, S: %.1f\r" % (pattern, color, speed))

    frametime = 1.0/FPS
    frames = max(1, int(FPS*speed))

    for frame in xrange(frames):
        start = time.time()
        #print("f: %s" % frame)
        bffr = ""
        # Hard run up
        if pattern == '1':
            tracker = LENGTH*frame/frames
            for led in xrange(LENGTH):
                (h,s,v) = (color, 0.7, 0.5) if led == int(tracker) else (0,0,0)
                (r,g,b) = utils.hsv2rgb(h,s,v)
                bffr += chr(r) + chr(g) + chr(b)
        # Hard run down
        elif pattern == '2':
            tracker = LENGTH*frame/frames
            for led in xrange(LENGTH):
                (h,s,v) = (color,0.7,0.5) if LENGTH - led - 1 == int(tracker) else (0,0,0)
                (r,g,b) = utils.hsv2rgb(h,s,v)
                bffr += chr(r) + chr(g) + chr(b)
        # Soft run up
        elif pattern == '3':
            for led in xrange(-2,LENGTH+1):
                v = float((LENGTH+3)*frame)/frames
                v = abs(2 + led - v)
                v = v + 1
                v = 1.0/v
                v **= 3
                #print("v: {}".format(v))
                (r,g,b) = utils.hsv2rgb(color, 0.7, v/2)
                #(r,g,b) = (0,0,0)
                bffr += chr(r) + chr(g) + chr(b)
            bffr = bffr[6:-3]
        # Soft run down
        elif pattern == '4':
            for led in xrange(-1, LENGTH+2):
                v = 1.0*((LENGTH+3)*frame)/frames
                v = abs(LENGTH - led - v + 1)
                v = v + 1
                v = 1.0/v
                v **= 3
                #print("v: {}".format(v))
                (r,g,b) = utils.hsv2rgb(color, 0.7, v/2)
                #(r,g,b) = (0,0,0)
                bffr += chr(r) + chr(g) + chr(b)
            bffr = bffr[3:-6]
        # Twinkle color
        elif pattern == '5':
            rnd = random.randint(0,3)
            rnd2 = random.randint(0,10)
            for led in xrange(LENGTH):
                (r,g,b) = (0,0,0)
                if frame % 2 and led == rnd and rnd2<6:
                    (r,g,b) = utils.hsv2rgb(color,0.7,1)
                bffr += chr(r) + chr(g) + chr(b)
        # Twinkle white
        elif pattern == '6':
            rnd = random.randint(0,3)
            rnd2 = random.randint(0,10)
            for led in xrange(LENGTH):
                (r,g,b) = (0,0,0)
                if frame % 2 and led == rnd and rnd2<6:
                    (r,g,b) = utils.hsv2rgb(0,0,1)
                bffr += chr(r) + chr(g) + chr(b)
        # Twinkle random color
        elif pattern == '7':
            rnd = random.randint(0,3)
            rnd2 = random.random()
            rndh = random.random()
            for led in xrange(LENGTH):
                (r,g,b) = (0,0,0)
                if frame % 2 and led == rnd and rnd2<.6:
                #if frame % 2 and random.random() < 0.3:
                    (r,g,b) = utils.hsv2rgb(rndh,1,1)
                bffr += chr(r) + chr(g) + chr(b)
        # Soft run up/down
        elif pattern == '8':
            f = abs(frame - (FPS*speed)/2)+(frames/LENGTH)
            for led in xrange(-2,LENGTH+1):
                v = 1.0*((LENGTH+3)*f)/(FPS*speed)
                v = abs(2 + led - v)
                v = v + 1
                v = 1.0/v
                v **= 3
                #print("v: {}".format(v))
                (r,g,b) = utils.hsv2rgb(color, 0.7, v/2)
                #(r,g,b) = (0,0,0)
                bffr += chr(r) + chr(g) + chr(b)
            bffr = bffr[6:-3]
        # One color hue cycle
        elif pattern == '9':
            h = frame/float(frames)
            for led in xrange(LENGTH):
                (r,g,b) = utils.hsv2rgb(h, 0.7, 0.5)
                bffr += chr(r) + chr(g) + chr(b)
        # One color value cycle
        elif pattern == '0':
            v = 1-abs((frame/float(frames))-0.5)*2
            v **= 4
            for led in xrange(LENGTH):
                (r,g,b) = utils.hsv2rgb(color, 0.7, v)
                bffr += chr(r) + chr(g) + chr(b)
        # Dark
        else:
            for led in xrange(LENGTH):
                (r,g,b) = (0,0,0)
                bffr += chr(r) + chr(g) + chr(b)

        sckt.send(bffr)
        sleep = start + frametime - time.time()
        if sleep > 0:
            time.sleep(sleep)
        #time.sleep(0.5)
    return


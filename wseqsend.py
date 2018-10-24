#!/usr/bin/python
import utils
import patterns
import sys
import time

if len(sys.argv) == 1:
    print(sys.argv[0] + " <file>")
    quit()
else:
    sequence = sys.argv[1]

start = time.time()
with open(sequence) as f:
    for line in f:
        (at, pattern, color, speed) = line.strip().split(' ')
        (m, s) = at.split(':')
        (s, ms) = s.split('.')
        at = start + int(m)*60 + int(s) + int(ms)/1000.0
        now = time.time()
        if at > now:
            time.sleep(at - now)
        #print("m: %s, s: %s, ms: %s, p: %s, c: %s, s: %s" % (m, s, ms, pattern, color, speed))
        sys.stdout.write("m: %s, s: %s, ms: %s, " % (m, s, ms))
        patterns.pattern(pattern, float(color), float(speed))


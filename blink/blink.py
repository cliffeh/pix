#!/usr/bin/env python3

# see: http://docs.pimoroni.com/blinkt/
import blinkt
import time

# reset 'em all
blinkt.clear()

# turn them all green, one at a time, one per second
for i in range(0, blinkt.NUM_PIXELS):
    blinkt.set_pixel(i, 0, 255, 0)
    blinkt.show()
    time.sleep(1)

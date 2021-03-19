## What's here?


### pix
A bash utility script (`pix`) for running things on all your Raspberry Pi nodes. It assumes that you've built your cluster, set up ssh keys (TODO: HOWTO), and (optionally, if you need to do things as root/some other user) configured sudo. Assuming all of that, usage is straightforward:

```
usage: pix [OPTIONS] COMMAND [-- ARGS]

  COMMAND will be run on each host, ARGS will be split
  between hosts and passed in one at a time

example:

  $ pix uname -n -- -r -v -m -o
  pi4: pi4 GNU/Linux
  pi2: pi2 #1333 SMP Mon Aug 10 16:51:40 BST 2020
  pi3: pi3 armv7l
  pi1: pi1 5.4.51-v7l+

options:
  -h, --help  print a brief help message and exit
```

### blink-test.py
Super-simple test script for the [Blinkt!](http://docs.pimoroni.com/blinkt/) Python library. Assuming you have blinkt installed (TODO: HOWTO) this little script will turn each LED green, one at a time.

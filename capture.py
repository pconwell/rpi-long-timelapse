from time import sleep
from datetime import datetime
from picamera import PiCamera as camera

cam = camera(resolution=(3280, 1845))

# Set ISO to the desired value
cam.iso = 50

# 'crop' the image to the area you want
# These settings don't seem to make sense in a logical way
# so you will just have to play with the numbers until you
# get what you want. Best I can tell, x + w needs to equal 1
# and y + h needs to equal 1 or you will distort the image.
#(x, y, h, w)
cam.zoom = (0.0, 0.25, .75, 1.0)

# Wait for the automatic gain control to settle
# If you remove this, the image exposure will be messed up
sleep(2)

# capture the image and name it as a timestamp
cam.capture('./shared/rpi-timelapse/%s.jpg' % datetime.now().strftime("%Y%m%d_%H%M"))
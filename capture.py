from time import sleep
from datetime import datetime
from picamera import PiCamera

camera = PiCamera(resolution=(1280, 720), framerate=30)
# Set ISO to the desired value
camera.iso = 100
# Wait for the automatic gain control to settle
sleep(2)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g
# Finally, take several photos with the fixed settings
#camera.capture_sequence(['image%s.jpg' % datetime.now().strftime("%Y%m%d_%H%M") for i in range(10)])
camera.capture_sequence(['./shared/rpi-timelapse/%s.jpg' % datetime.now().strftime("%Y%m%d_%H%M") for i in range(10)])

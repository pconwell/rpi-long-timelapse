from time import sleep
from datetime import datetime
from picamera import PiCamera as camera
import pandas as pd

# read the sunrise/sunset csv into a pandas dataframe

df = pd.read_csv('./nashville.csv')

# find the sunrise and sunset times for today's date:
sunrise = df.loc[df['date'] == datetime.today().strftime("%Y-%m-%d")].values.tolist()[0][4]
sunset = df.loc[df['date'] == datetime.today().strftime("%Y-%m-%d")].values.tolist()[0][5]

# convert sunrise and sunset to datetime objects (there is almost certainly a better way to do this):
sunrise = datetime.strptime(datetime.today().strftime("%Y-%m-%d") + " " + sunrise, "%Y-%m-%d %H:%M")
sunset = datetime.strptime(datetime.today().strftime("%Y-%m-%d") + " " + sunset, "%Y-%m-%d %H:%M")

if datetime.now() > sunrise and datetime.now() < sunset:

cam = camera(resolution=(3280, 1845))

# Set ISO to the desired value
cam.iso = 50

# 'crop' the image to the area you want.
# These settings don't make sense to me in a logical way so you will
# just have to play with the numbers until you get what you want.
# The below setting, for example, will crop the image to the lower right part of the image.
# In other words, the left and top portion of the image will be removed.
# Best I can tell, x + w needs to equal 1 and y + h needs to equal 1 or you will distort the image.
# zoom = (x, y, h, w)
cam.zoom = (0.0, 0.25, .75, 1.0)

# Wait for the automatic gain control to settle
# If you remove this, the image exposure will be messed up
sleep(2)

# capture the image and name it as a timestamp
cam.capture('./shared/rpi-timelapse/%s.jpg' % datetime.now().strftime("%Y%m%d_%H%M"))

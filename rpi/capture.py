from time import sleep
import datetime
from picamera import PiCamera as camera
#import pandas as pd
import csv


# read the csv file (for sunrise/sunset times)
csv_file = csv.DictReader(open('nashville.csv', 'r'))

# read through each row in the csv file
for row in csv_file:

        # if the row matches today's date...
        if datetime.datetime.strptime(row['date'], "%Y-%m-%d").date() == datetime.datetime.today().date():

                # then get the sunrise and sunset times and break the loop
                sunrise = datetime.time(int(row['sunrise'].split(":")[0]),int(row['sunrise'].split(":")[1]))
                sunset = datetime.time(int(row['sunset'].split(":")[0]),int(row['sunset'].split(":")[1]))
                break

# check if the current time right now is after sunrise and before sunset
if datetime.datetime.now().time() > sunrise and datetime.datetime.now().time() < sunset:

        #if true, take a picture
        cam = camera(resolution=(3280, 1845))

        # Set ISO to the desired value
        #cam.iso = 50
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
        cam.capture(f'/home/pi/images/{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.jpg')

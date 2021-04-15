from time import sleep
import datetime
from picamera import PiCamera
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
        camera = PiCamera()

        # set resolution
        camera.resolution=(3280, 1845)

        # Wait for the automatic gain control to settle
        # If you remove this, the image exposure will be messed up
        sleep(3)

        # capture the image and name it as a timestamp
        camera.capture(f'/home/pi/images/{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.jpg')

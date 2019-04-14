#!/bin/bash

DATE=$(date +"%Y%m%d_%H%M")

raspistill --output /home/pi/shared/rpi-timelapse/$DATE.jpg --burst --nopreview

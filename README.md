# rpi-long-timelapse
raspberry pi year long timelapse

This project will set up a long-term time lapse with an unknown end date. The project will assume that the timelapse will be approximatley a year long, but this project should be scaleable to any duration AS LONG AS you have enough storage space. There are many factors that go into creating a timelapse, but a ballpark figure is to expect the file size *before* creating the final video (i.e. the source photos) to be approximately 2 TB. Depending on your particular setup, don't be suprized if it's much larger.

## What you need

Things you need to have:
- Raspberry pi (I am using the pi zero w)
- Raspberry pi camera module (I am using the v2 module)
- pi zero camera ribbon cable (if you are using the pi zero)
- Micro USB power cord & USB power source
- Micro SD card w/ Raspbian installed (Pretty much any micro SD should work, but I am using the SanDisk Extreme PRO 32 GB)
- Somewhere to store vast number of photos (SD card won't hold enough - I am using a samba networked file share)
- (optional) a case for the pi

Things you need to know:
- How to flash raspbian on to the SD card
- How to edit config files on the SD card (to set up wifi and ssh)
- How to find the rpi's IP address on your router/DHCP server
- How to SSH into the rpi
- How to run basic commands from CLI (we will not be using a GUI for anything)
- How to mount a share/network drive (samba & fstab)
- How to set up a cron job



## Initial Setup
I will be using a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) and a [camera module](https://www.raspberrypi.org/products/camera-module-v2/). Make sure you also get the correct cable as the camera module is compatable with both the full size pi and pi zero - but the cables are different between the full size and the zero. I ordered [this kit](https://www.adafruit.com/product/3414), which comes with everything you need except for a micro SD card. Pretty much any SD card should do fine, but I'm using [this one](https://www.amazon.com/gp/product/B06XYHN68L) which I honestly don't know much about other than it was relatively cheap and was recommended online for use with the pi.

If you are not familiar with the pi zero, it does not have an ethernet port and only has mini hdmi and micro usb ports. If you have the adapters already, no big deal. But, I don't have the correct adapters and I don't want to double the price of this project by buying adapters I'll use once. So, we will need to set up wifi and ssh in a somewhat unique way.

> side note - the camera will probably be out of focus depending on the distance to your subject. Don't do like I did - spend the 97¢ on the camera adjustment tool. I tried to use a pair of needle nose pliers, my hand slipped and I scratched the lens.

### Raspbian

https://www.raspberrypi.org/downloads/raspbian/

https://www.balena.io/etcher/

1. Flash raspbian to SD card
2. Open/mount SD card on desktop and navigate to /boot/
3. Create `/wpa_supplicant.conf` with below contents, replacing the values as necessary
4. Create empty file named `ssh` (`$ touch /boot/ssh`)
5. Eject SD card and put SD card into pi
6. Power up pi
7. Find pi's IP address in your router/DHCP
8. SSH into pi (pi@IP:raspberry)
9. `$ sudo raspi-config` and enable camera
10. reboot
11. `$ nano /etc/fstab`
12. `$ sudo mount -a`
13. test camera: `raspistill -o ~/shared/cam.jpg`

### Wifi

`/boot/wpa_supplicant.conf`

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=«your_ISO-3166-1_two-letter_country_code»

network={
    ssid="«your_SSID»"
    psk="«your_PSK»"
    key_mgmt=WPA-PSK
}
```

### fstab
Here we are setting up a network share because we won't be able to hold terabytes worth of information on the raspberry pi itself. You will need to set up a shared drive somehow, which I will currently not cover here. Just for sake of example, my network share is a samba share drive running on an ubuntu host. The host server is at IP `192.168.1.25` and the shared directory is `/shared`. Here I have mounted the network share drive at `/home/pi/shared` on the raspberry pi. Now, if I tell the raspberry pi to save a photo to `/home/pi/shared` it is *really* saving the picture to the network server at `//192.168.1.25/shared`. Setting up a network drive gives me several advantages. 1) Like I said, the rpi cannot hold TB of data, 2) I can easily manipulate the files remotely now, and 3) I can more easily create backups of the photos. I'd really hate to get 6 months into this project then lose data if my harddrive goes out.

`//192.168.1.25/shared  /home/pi/shared cifs guest,uid=1000,iocharset=utf8 0 0`

## Additional Settings
Once it looks like you can boot up and sign in to the pi, and t he camera is working, you can tweak some other settings in `$ sudo raspi-config` such as setting your locale, changing your password (highly recommended), etc.

Since we will be using this rpi completely headlessly (i.e. only though SSH/CLI and not using a GUI), I would recommend the following settings/tweaks inside raspi-config:

1. Run update
2. Advanced -> expand storage (might be optional depending on the size of your SD card. A 32 GB card did not apparently need to be expanded)
3. Advanced -> memory split -> 16 MB
4. Interface -> Camera -> On (should already be on)
5. Interface -> SSH -> On (should already be on)
6. Interface -> Everthing else -> Off (Should alredy be off, so shouldn't need to change)
7. Localization -> Change settings according to your language/location/timezone/etc
8. Boot Option -> Desktop/CLI -> Console Autologin (since we are not using the GUI, this disables the GUI and frees up a good chunk of RAM)
9.  Boot Options -> Wait for Network at Boot -> Disabled (You may be able to enable this, but I'm not sure how well this will cooperate with wifi so I disabled this setting. I don't want it to hang if it can't immediately connect to wifi for some reason.)
10. Unless you have other specific changes you need/want, exit raspi-config  

`$ sudo shutdown now -r` for good measure

## Camera Setup
> https://www.raspberrypi.org/documentation/raspbian/applications/camera.md

> `$ sudo apt install python3-picamera`
> `$ sudo apt install python3-pandas`

> pandas adds a decent amount of overhead, but it will make working with the csv sunrise/sunset file easier. If you are really trying to make this as simple, efficient and streamlined as possible you can do away with pandas. But I'm lazy, it works, and this rpi is doing nothing but taking a picture every one minute so I'm not too concerned with the overhead.

We should mostly be up and running at this point, time to test the camera.

`$ raspistill --output ~/shared/rpi-timelapse/image.jpg`

Remember, I am using a shared network drive to store the images. So adjust the output location to wherever you are going to store your images. If you wanted to store the images on the internal SD card, you could use something like `./image.jpg` or `./images/image.jpg` instead.

You will likely need to adjust your focus. Using the focus tool you bought (you bought one, right?), adjust the focus and take another picture. This can be a bit time consuming, but you really want to make sure the camera is properly focused because once we get it focused and mounted, we won't touch the camera itself again for a long time. Once the camera is focused and mounted, everything else we will do is on the software side. So take your time here and make sure you are happy with your physical set up.





----

Don't bother with anything below here ...

----


Depending on what exactly you are wanting to do, the camera setup can either be really easy and straight forward, or it can be fairly invovled. Let's start with just taking a series of photos over a 5 minute period (one picture every 60 seconds) to see if that will work:

`$ raspistill --timeout 300000 --timelapse 60000 --output ~/shared/rpi-timelapse/image%04d.jpg`

If that seems to work, let's try a 12 hour timelapse. The demo we just created is (depending on your settings) less than one second long, so we need a longer demo to make sure it's working correctly.

`$ raspistill --timeout 43200000 --timelapse 60000 --output ~/shared/rpi-timelapse/image%06d.jpg`

Remember, we are measuring in milliseconds, so 12 hours x 60 minutes x 60 seconds x 1000 (milliseconds) == 43200000. I've also changed the filename output from `%04` to `%06` so we don't evetually start overwritting our first photos (even though 4 digits would have given us 10,000 photos, which should last approximately 166 hours or one week... but if we are going to take a year long timelapse we need to plan ahead).

Another issue we need to think about is what happens if we lose our SSH session (network drops, computer freezes, power goes out, etc, etc). For now, let's use screen so we can detach our session. Later on, we will use some type of automation (probably cron) to schedule the pictures long term for us. We need to think about redudancy and automation - how will we recover if the power goes out, for example? Over the span of a year, it is likely that the power or network will go out at least once. But, for now, let's assume everthing will keep working for the next twelve hours and just add `screen` to our toolbag.

1. `$ ssh [rpi IP]`
2. `$ sudo apt install screen`
3. `$ screen`
4. `$ raspistill --timeout 43200000 --timelapse 60000 --output ~/shared/rpi-timelapse/image%06d.jpg`
5. `[ctrl]+[a]` then `[d]` to detach session
6. To reattach to a screen session `$ screen -r`

There is much more you can do with screen, but for now this is all we need. Feel free to learn more about it.

> Note to self, so far the 12 hour test has not been sucessful. The seriese of photos will error out after 15 - 30 minutes. There does not seem to be a consistant error so far. The last run just stopped working after 26 captures. The raspistill process seems to be still running but it just stopped producing photos. My first guess is that the power supply I am currently using will output 0.5 A but I believe (I haven't tested this) that the rpi zero needs about 0.7 A to run with wifi and an additional ~150 mA each time it captures a photo. So I'm guessing (hoping) that the power supply is the problem.

> I'll hunt down another power supply later (I've got a bunch, just don't want to hunt them down before going to work). In the meantime, I'm going to try adding `--burst` and `--nopreview`. I don't think that will make a difference, but they are probably options I should use anyway to reduce overhead so I'll try them out. Once I get back from work, I will find a spare 2 A USB power supply and see if that makes a difference.

> Timelapse still doesn't seem to work very well, even with a 2.4 A power supply. It still gives out after about 20 minutes or so. I'm going to try it with crontab every minute.

> Okay, we are skipping ahead in our testing and going straight to bash and cron. Running the command directly in cron would not name the files correctly. So we are going to set up a cron job to run a bash script. The bash script will take a single picture and name the file the date and time. The cron job will run every one minute.

Bash:
```bash
#!/bin/bash

DATE=$(date +"%Y%m%d_%H%M")

raspistill --output /home/pi/shared/rpi-timelapse/$DATE.jpg --burst --nopreview
```

Cron:
```
* * * * * /home/pi/timelapse.sh
```


----

 ... and above here

----





## Scheduling Photos

## Storing Photos

## Power / Storage redudancy

## Create Timelapse

## Links
https://www.raspberrypi.org/documentation/raspbian/applications/camera.md
https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md
https://www.raspberrypi.org/documentation/hardware/camera/README.md
https://www.raspberrypi.org/documentation/usage/camera/raspicam/timelapse.md
https://www.raspberrypi.org/products/camera-module-v2/

https://picamera.readthedocs.io/en/release-1.13/index.html

# rpi-long-timelapse
raspberry pi year long timelapse

This project will set up a long-term time lapse with an unknown end date. The project will assume that the timelapse will be approximatley a year long, but this project should be scaleable to any duration AS LONG AS you have enough storage space. There are many factors that go into creating a timelapse, but a ballpark figure is to expect the file size *before* creating the final video (i.e. the source photos) to be approximately 2 TB. Depending on your particular setup, don't be suprized if it's much larger.

## Initial Setup
I will be using a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) and a [camera module](https://www.raspberrypi.org/products/camera-module-v2/). Make sure you also get the correct cable as the camera module is compatable with both the full size pi and pi zero - but the cables are different between the full size and the zero. I ordered [this kit](https://www.adafruit.com/product/3414), which comes with everything you need except for a micro SD card. Pretty much any SD card should do fine, but I'm using [this one](https://www.amazon.com/gp/product/B06XYHN68L) which I honestly don't know much about other than it was relatively cheap and was recommended online for use with the pi.

If you are not familiar with the pi zero, it does not have an ethernet port and only has mini hdmi and micro usb ports. If you have the adapters already, no big deal. But, I don't have the correct adapters and I don't want to double the price of this project by buying adapters I'll use once. So, we will need to set up wifi and ssh in a somewhat unique way.

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
Once it looks like you can boot up and sign in to the pi, and the camera is working, you can tweak some other settings in `$ sudo raspi-config` such as setting your locale, changing your password (highly recommended), etc.

Since we will be using this rpi completely headlessly (i.e. only though SSH/CLI and not using a GUI), I would recommend the following settings/tweaks inside raspi-config:

1. Run update
2. Advanced -> expand storage (might be optional depending on the size of your SD card. A 32 GB card did not apparently need to be expanded)
3. Advanced -> memory split -> 16 MB
4. Interface -> Camera -> On (should already be on)
5. Interface -> SSH -> On (should already be on)
6. Interface -> Everthing else -> Off (Should alredy be off, so shouldn't need to change)
7. Localization -> Change settings according to your language/location/timezone/etc
8. Unless you have other specific changes you need/want, exit raspi-config  

`$ sudo shutdown now -r` for good measure

## Camera Setup
> https://www.raspberrypi.org/documentation/raspbian/applications/camera.md

Depending on what exactly you are wanting to do, the camera setup can either be really easy and straight forward, or it can be fairly invovled. Let's start with just taking a series of photos over a 5 minute period (one picture every 60 seconds) to see if that will work:

`$ raspistill --timeout 300000 --timelapse 60000 --output ~/shared/rpi-timelapse/image%04d.jpg`

If that seems to work, let's try a 12 hour timelapse. The demo we just created is (depending on your settings) less than one second long, so we need a longer demo to make sure it's working correctly.

`$ raspistill --timeout 43200000 --timelapse 60000 --output ~/shared/rpi-timelapse/image%06d.jpg`

Remember, we are measuring in milliseconds, so 12 hours x 60 minutes x 60 seconds x 1000 (milliseconds) == 43200000. I've also changed the filename output from `%04` to `%06` so we don't evetually start overwritting our first photos (even though 4 digits would have given us 10,000 photos, which should last approximately 166 hours or one week... but if we are going to take a year long timelapse we need to plan ahead).



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

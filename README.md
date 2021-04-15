# rpi-long-timelapse
raspberry pi year long timelapse

This project will set up a long-term time lapse. This project should be scaleable to any duration *AS LONG AS* you have enough storage space to hold all the images needed to create the timelapse.


## What you need

Things you need to have:
- Raspberry pi (I am using the pi zero w)
- Raspberry pi camera module (I am using the v2 module)
- pi zero camera ribbon cable (if you are using the pi zero. You will need the normal ribbon cable if you are using the full size pi)
- Micro USB power cord & USB power source of at least 1000 mA
- Micro SD card w/ Raspbian installed (Pretty much any micro SD should work, but I am using the SanDisk Extreme PRO 32 GB)
- Somewhere to store vast number of photos (SD card won't hold enough - I am using a samba networked file share)
- (optional) a case for the pi
- (optional) an rpi camera focus tool (highly recommended)

Things you need to know:
- How to flash raspbian on to the SD card
- How to edit config files on the SD card (to set up wifi and ssh)
- How to find the rpi's IP address on your router/DHCP server
- How to SSH into the rpi
- How to run basic commands from CLI (we will not be using a GUI for anything)
- How to mount a share/network drive (samba & fstab)
- How to set up a cron job
- Basic Python programing


## Initial Setup
I will be using a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) and a [camera module](https://www.raspberrypi.org/products/camera-module-v2/). Make sure you also get the correct cable as the camera module is compatable with both the full size pi and pi zero - but the cables are different between the full size and the zero. I ordered [this kit](https://www.adafruit.com/product/3414), which comes with everything you need except for a micro SD card, the camera focusing tool, and the usb cable and power supply. Pretty much any SD card should do fine, but I'm using [this one](https://www.amazon.com/gp/product/B06XYHN68L) which I honestly don't know much about other than it was relatively cheap and was recommended for use with the pi.

If you are not familiar with the pi zero, it does not have an ethernet port and only has mini hdmi and micro usb ports. If you have the adapters already, no big deal. But, I don't have the correct adapters and I don't want to double the price of this project by buying adapters I'll use once. So, we will need to set up wifi and ssh in a somewhat unique way.


### Raspbian

https://www.raspberrypi.org/downloads/raspbian/

https://www.balena.io/etcher/

1. Flash raspbian to SD card. I used [Etcher](https://www.balena.io/etcher/).
2. Open/mount SD card on desktop and navigate to /boot/
3. Create `/wpa_supplicant.conf` with below contents, replacing the values as necessary
4. Create empty file named `ssh` (`$ touch /boot/ssh`)
5. Eject SD card and put SD card into pi
6. Power up pi
7. Find pi's IP address in your router/DHCP
8. SSH into pi (pi@IP:raspberry)
9. `$ sudo raspi-config` and enable camera
10. reboot
11. `$ nano /etc/fstab` (See Below)
12. `$ sudo mount -a` to mount the share drive added to fstab.
13. test camera: `raspistill -o ~/shared/rpi-timelapse/image.jpg`

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
~~Here we are setting up a network share because we won't be able to hold terabytes worth of information on the raspberry pi itself. You will need to set up a shared drive somehow, which I will currently not cover here. ~~

~~But, for the sake of example, my network share is a samba share drive running on an ubuntu host. The host server is at IP `192.168.1.25` and the shared directory is `/shared`. Here I have mounted the network share drive at `/home/pi/shared` on the raspberry pi. Now, if I tell the raspberry pi to save a photo to `/home/pi/shared` it is *really* saving the picture to the network server at `//192.168.1.25/shared`. Setting up a network drive gives me several advantages. 1) Like I said, the rpi cannot hold TB of data, 2) I can easily manipulate the files remotely now, and 3) I can more easily create backups of the photos. I'd really hate to get 6 months into this project then lose data if my HDD/SD goes out. Here is the line I'll add to `fstab` on the rpi.~~

Set up an NFS file server as desired (I'm using unRaid). Then use the following fstab.

~~`//192.168.1.25/shared  /home/pi/shared cifs guest,uid=1000,iocharset=utf8 0 0`~~

192.168.1.23:/mnt/user/timelapse   /mnt/unraid/timelapse nfs defaults 0 0

~~And here is the Samba config settings on the server:~~

~~```
[shared]
browseable = yes
path = /shared/
guest ok = yes
force user = pconwell
force group = pconwell
read only = no
create mask = 664
force create mode = 644
directory mask = 755
force directory mode = 755
```~~

NFS tends to have issues going stale, especially over wifi. So we can use an ugly, hackish script to check on the nfs connection every 60 seconds:

```
#!/bin/bash

# crontab:
#* * * * * /root/fix_stale_nfs.sh >/dev/null 2>&1

list=$(ls /mnt/unraid)

for i in $list
do
        status=$(ls /mnt/unraid/$i 2>&1)

        if [[ $status =~ .*Stale.* ]]
                then
                umount -f /mnt/unraid/$i
        fi
done

mount -a
```

And then use `sudo crontab -e` to run the script as desired. Don't forget to make the script executable with `chmod +x` or the script won't work (even though the logs won't show you any errors).

## Additional Settings
Since we will be using this rpi completely headlessly (i.e. only though SSH/CLI and not using a GUI), I would recommend the following settings/tweaks inside `$ raspi-config`:

1. Run update
2. Advanced -> expand storage (might be optional depending on the size of your SD card. A 32 GB card did not apparently need to be expanded)
3. Advanced -> memory split -> 16 MB
4. Interface -> Camera -> On (should already be on)
5. Interface -> SSH -> On (should already be on)
6. Interface -> Everthing else -> Off (Should alredy be off, so shouldn't need to change)
7. Localization -> Change settings according to your language/location/timezone/etc
8. Boot Option -> Desktop/CLI -> Console Autologin (since we are not using the GUI, this disables the GUI and frees up a good chunk of RAM)
9.  Boot Options -> Wait for Network at Boot -> Enabled (This could potentially cause an issue, but I don't have a good fool-proof solution. Since we are not using wired ethernet, we are going to have to wait for wifi to connect. If wifi doesn't connect for some reason, we could get hung during boot. But, if we don't wait for boot, the network drive probably won't auto-mount. One thing I haven't been able to find in the documentation is what happens if it cannot connect to the network. Does it fail and hang? Does it eventally boot anyway? I don't know...)
10. Unless you have other specific changes you need/want, exit raspi-config  

`$ sudo shutdown now -r` for good measure

## Camera Setup
> https://www.raspberrypi.org/documentation/raspbian/applications/camera.md

> side note - the camera will probably be out of focus depending on the distance to your subject. Don't do like I did - spend the 95¢ on the camera adjustment tool. I tried to use a pair of needle nose pliers, my hand slipped and I scratched the lens. I highly recommend you spend the extra 95¢ so you don't have to spend $30 on a replacement camera module.

We should mostly be up and running at this point, time to test the camera.

`$ raspistill --output ~/shared/rpi-timelapse/image.jpg`

Remember, I am using a shared network drive to store the images. So adjust the output location to wherever you are going to store your images. If you wanted to store the images on the internal SD card, you could use something like `./image.jpg` or `./images/image.jpg` instead.

You will likely need to adjust your focus. Using the focus tool you bought (you bought one, right?), adjust the focus and take another picture. This can be a bit time consuming, but you really want to make sure the camera is properly focused because once we get it focused and mounted, we won't touch the camera itself again for a long time. Once the camera is focused and mounted, everything else we will do is on the software side. So take your time here and make sure you are happy with your physical set up.

Once you have the camera focused properly, mount it however you deem acceptable. Mine is taped to the inside of a window using gaff tape. From here on out, everything is done in software.


## Scheduling Photos
We will be using python to manage most of the picture taking. Once we get a script made, we will use `crontab` to execute the python script every 60 seconds. Python3 should already be installed (make sure you are using `python3` and not `python`), but we will need to install two additional libraries:

`$ sudo apt install python3-picamera`
`$ sudo apt install python3-pandas`

Pandas adds a decent amount of overhead, but it will make working with the csv sunrise/sunset file easier. If you are really trying to make this as simple, efficient and streamlined as possible you can do away with pandas. But I'm lazy, it works, and this rpi is doing nothing but taking a picture every one minute so I'm not too concerned with the overhead.

But that being said, (1) the rpi zero is pretty low powered, and (2) pandas adds a non-trivial amount of overhead, and (3) writing to a network share over wifi adds overhead as well, so with this particular setup it takes a good 20 seconds per picture. If you are taking a picture more frequently than once per minute it may be an issue. We could increase efficency by (1) getting rid of pandas and parsing the csv without pandas, (2) write the image to the SD card then move the image(s) during non peak times (like midnight for example). For now, this works for my needs so I currently do not plan to fix these problems.

Scheduling the photos is pretty straight forward. We just need to set a cronjob to execute our python script every one minute. We could probably be more efficent if we just had one python script that scheduled the captures for us, but my concern is redudancy. What if the power goes out? How will the python script recover? Will it start at boot? What if the network is down? Will the python script fail with an error? What if something unexpected happens and the script fails? How will the script recover and start capturing images again? I think the best way around all these issues is to just execute the script every 60 seconds. Yes, it adds overhead with importing pandas every time, etc... but it's (I think) the best way to make sure the images are being captured.

`$ crontab -e`

`* * * * * /home/pi/capture.py`

The `capture.py` script is fairly straight foward as well. It reads from a csv listing sunrise and sunset times for a certain location. It then checks if the current time is after sunrise but before sunset for a given day. If it is between sunrise and sunset, it will capture an image. That's pretty much it - like I said, not much to it.

> Note: the raspistill function seems fine for capturing a signle image, but I had a lot of issues using `raspistill --timelapse`. I was unable to produce more than about 20 images before the process would fail. If you want to take pictures around the clock then raspistill will probably work fine but I still wouldn't recommend using `raspistill --timelapse` unless you are making a really short timelapse. I would still recommend executing raspistill with crontab. I'm using python here mainly to read through the csv and determine if it's daylight or not.

## Storing Photos

> redundancy & backups here

> crashplan

In my particular setup, I will only be taking pictures between sunrise and sunset (so let's assume an average of 12 hours per day) and I will be taking one picture per minute. The individual images are approximately 5 MB. So, roughly we can expect 12 x 60 x 5 = **3,600 MB / day** for storage needs. I am speculating that my project will last about one year, so 1.3 TB or so total storage will be needed. I would prepare at least twice what you think you will need to be safe.

This storage requirement also is *only* the images themselves. You will also need some working space to make the actual timelapse video once you combine all the images. My best guess currently is I will need about 70 GBs for my year long timelapse video.

## Power / Storage redudancy

> probably not going to worry about power redundancy right now because (1) the power rarely goes out here, and (2) if/when it does go out it's only for short durations, and (3) once the power comes back on it will automatically boot back up and start taking pictures again.

> One consideration I need to keep in mind is the server that hosts the samaba share takes about 15 minutes to boot up and I don't currently have it on a UPS (I know, I know!), so if there is a power failure, the rpi will be fine but the network share won't exist and there is (currently) no good way to re-mount the network share automatically. This *will* need to be addressed. Intial thought is to save the images to the internal SD card then move the images at night AND if the network is up. If the network is down, reboot the pi and try again?

## Create Timelapse

> This I know very little about, so if you know a better process you may want to use it instead.

```shell
$ ls *.jpg > stills.txt
$ mencoder -nosound -ovc lavc -lavcopts vcodec=mpeg4:aspect=16/9:vbitrate=64000000 -vf scale=3280:2460 -o timelapse.avi -mf type=jpeg:fps=24 mf://@stills.txt
```

## Links
https://www.raspberrypi.org/documentation/raspbian/applications/camera.md
https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md
https://www.raspberrypi.org/documentation/hardware/camera/README.md
https://www.raspberrypi.org/documentation/usage/camera/raspicam/timelapse.md
https://www.raspberrypi.org/products/camera-module-v2/

https://picamera.readthedocs.io/en/release-1.13/index.html

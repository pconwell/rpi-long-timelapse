# rpi-long-timelapse
raspberry pi year long timelapse

This project will set up a long-term time lapse with an unknown end date. The project will assume that the timelapse will be approximatley a year long, but this project should be scaleable to any duration AS LONG AS you have enough storage space. There are many factors that go into creating a timelapse, but a ballpark figure is to expect the file size *before* creating the final video (i.e. the source photos) to be approximately 1 TB. Depending on your particular setup, don't be suprized if it's 2 or 4 TB.

## Initial Setup
I will be using a [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/) and a [camera module](https://www.raspberrypi.org/products/camera-module-v2/). Make sure you also get the correct cable as the camera module is compatable with both the full size pi and pi zero - but the cables are different between the full size and the zero. I ordered [this kit](https://www.adafruit.com/product/3414), which comes with everything you need except for a micro SD card. Pretty much any SD card should do fine, but I'm using [this one](https://www.amazon.com/gp/product/B06XYHN68L) which I honestly don't know much about other than it was relatively cheap and was recommended online for use with the pi.

If you are not familiar with the pi zero, it does not have an ethernet port and only has mini hdmi and micro usb ports. If you have the adapters already, no big deal. But, I don't have the correct adapters and I don't want to double the price of this project by buying adapters I'll use once. So, we will need to set up wifi and ssh in a somewhat unique way.

### Raspbian

sdfj kl;gj l;fg

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

### SSH
`touch /boot/ssh`

## Camera Setup

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

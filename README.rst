Hardware Customer Display
=========================

Python library for supporting Customer Point Of Sale Display.

It should support most serial and USB-serial LCD displays out-of-the-box
or with inheritance of a few functions.

It has been tested with:

* Bixolon BCD-2000 (Datasheet: https://www.bixolon.com/product_view.php?idx=162 To be used in BCD-2000K config mode)
* Bixolon BCD-1100 (Discontinued by Bixolon. Support page: https://www.bixolon.com/download_view.php?idx=78)
* Bixolon BCD-1000 (Discontinued by Bixolon. Support page: https://www.bixolon.com/download_view.php?idx=78)
* Epson DM-D110 (model M58DB)
* Epson OCD300 : http://www.aures-support.fr/NEWSITE/afficheurs-ocd100150

For Epson OCD300, change pywebdriver/config/config.ini :

```
[display_driver]
device_name=/dev/ttyACM0
```

For Bixolon devices connected via USB, for kernel >= 3.12, you have to create a file /etc/udev/rules.d/99-pyposdisplay.rules with the following content:

```
ACTION=="add", ATTRS{idVendor}=="1504", ATTRS{idProduct}=="0011", RUN+="/sbin/modprobe ftdi_sio", RUN+="/bin/sh -c 'echo 1504 0011 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id'"
ACTION=="add", ATTRS{idVendor}=="1504", ATTRS{idProduct}=="008c", RUN+="/sbin/modprobe -q ftdi_sio" RUN+="/bin/sh -c 'echo 1504 008c > /sys/bus/usb-serial/drivers/ftdi_sio/new_id'"
```
(Source : http://www.leniwiec.org/en/2014/06/25/ubuntu-14-04lts-how-to-pass-id-vendor-and-id-product-to-ftdi_sio-driver/)


For kernel < 3.12 and bixolon display please read this: http://techtuxwords.blogspot.fr/2012/12/linux-and-bixolon-bcd-1100.html


This library has been inspired by the work carried out during a POS code sprint at Akretion France
from July 7th to July 10th 2014.

Contributors
============

* Alexis de Lattre <alexis.delattre@akretion.com>
* Sébastien BEAU <sebastien.beau@akretion.com>

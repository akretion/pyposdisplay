Hardware Customer Display
=========================

Python library for supporting Customer Point Of Sale Display.

It should support most serial and USB-serial LCD displays out-of-the-box
or with inheritance of a few functions.

It has been tested with:

* Bixolon BCD-1100 (Datasheet : http://www.bixolon.com/html/en/product/product_detail.xhtml?prod_id=61)
* Bixolon BCD-1000
* Epson DM-D110 (model M58DB)


For kernel <= 3.12 you have to add this code in /etc/udev/99-pyposdisplay.rules

```
ACTION=="add", ATTRS{idVendor}=="1504", ATTRS{idProduct}=="0011", RUN+="/sbin/modprobe ftdi_sio", RUN+="/bin/sh -c 'echo 1504 0011 > /sys/bus/usb-serial/drivers/ftdi_sio/new_id'"
```
(Source : http://www.leniwiec.org/en/2014/06/25/ubuntu-14-04lts-how-to-pass-id-vendor-and-id-product-to-ftdi_sio-driver/)


For kernel < 3.12 and bixolon display please read this: http://techtuxwords.blogspot.fr/2012/12/linux-and-bixolon-bcd-1100.html


This library has been inspired by the work carried out during a POS code sprint at Akretion France
from July 7th to July 10th 2014.

Contributor
=============
* Alexis de Lattre <alexis.delattre@akretion.com>
* Sébastien BEAU <sebastien.beau@akretion.com>

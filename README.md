pi-adac
=======

Driver and examples for the Raspberry Pi ADAC expansion board

A brief description on how to install the spi package.
The rest of the documentation can be found att: http://tightdev.net/SpiDev_Doc.pdf

SPI installation
First things first, itâ' always the best to keep your Raspberry Pi up to date, otherwise some
things here may not work. Open a new console and execute the following commands:

> sudo apt-get update && sudo apt-get upgrade && sudo reboot

If you haven't done this yet, grab some coffee or something else because this may take up
to an hour or two.

If you haven't installed it already you need to install the Python Dev package:

> sudo apt-get install python-dev

You need to be sure that SPI is enabled in your system (it is disabled by default because 
it is rarely used). Open a new terminal and enter:

> sudo nano/etc/modprobe.d/raspi-blacklist.conf

This will open a text editor. You should see a line like this in this file:

* spi-bcm2708

Put a # before this line to comment it out. Save (Ctrl+O) and exit (Ctrl+X). After a reboot the
device should be found.

sudo reboot
# --- after reboot type ---
lsmod

In the list lsmod outputs you should find the entry "spi_bcm2708" now.

To install the SPI driver you need to have downloaded the pi-adac package from github. You
can either clone the repository using the following command:

> git clone https://github.com/Sweet-Peas/pi-adac.git

or alternatively you can simply download the zip file and extract it into a working directory.

To install the python spi binding type the following into a terminal window located in the
source package that you've downloaded.

sudo python setup.py install

After a few seconds the python spi binding is installed and you can start running the example 
python programs in the python sub directory.


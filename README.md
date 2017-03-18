# cec-daemon
CEC Daemon to control CEC devices

##Setup
###Access to cec device.

Tested on Freescale Cubox-i on Arch Alarm.
Need to install libcec for im6 devices for cec device to work. Will change for different devices/distros.

Set up "cec" group and add user to group.
Set up udev rule to set the group and permissions on the cec device.
The device on the Cubox-i is at "/dev/mxc_hdmi_cec".

~~~
/etc/udev/rules.d/99-cec-rules

KERNEL=="mxc_hdmi_cec", SUBSYSTEM=="mxc_hdmi_cec", GROUP="cec", MODE="0660"
~~~

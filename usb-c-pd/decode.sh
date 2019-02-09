#!/bin/sh

sigrok-cli -P "usb_power_delivery:cc1=0" -A "usb_power_delivery=payload" -i "$1"

exit $?

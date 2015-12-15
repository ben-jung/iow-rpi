# KAIST 2015 Fall CS492c Project iow-rpi

1. write your KAIST portal ID and password in etc/wpa_supplicant/wpa_supplicant.conf
2. reboot
3. git clone it to raspberry pi
4. set machine ID and server URL in sensor.py
5. connect ADXL345 accelerometer to raspberry pi
(http://www.stuffaboutcode.com/2014/06/raspberry-pi-adxl345-accelerometer.html)
6. if you want to use BLE beacon, install bluez 5.30 and set BLE_USED to True
7. run as "sudo python sensor.py"

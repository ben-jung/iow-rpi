# ADXL345 Python Check Vibration 
#
# author:  Ben Jung
# license: BSD 

from adxl345 import ADXL345
from math import sqrt
from subprocess import call, Popen
import time
import requests


URL = 'http://admin.kaist.ac.kr:3535/get_data?'
ID = '2'
ON_OFF_STANDARD = 0.20
SLEEP_DELAY = 0.1
ACCUMULATED_NUMBER = 10
ACCUMULATED_STANDARD = 5

# Fixed hex
BLE_HEX_FIXED_FORWARD = 'sudo hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 1A 1A FF 4C 00 02 15 E2 0A 39 F4 73 F5 4B C4 A1 2F 17 D1 AD 07 A9 61 '
# Major (Machine id)
BLE_HEX_MACHINE_ID = '00 0' + ID + ' '
# Minor (State 0: idle, 1: running)
BLE_HEX_STATE_IDLE = '00 00 '
BLE_HEX_STATE_RUN = '00 01 '
BLE_HEX_FIXED_BACK = 'C8 00 '


def check_onoff(adxl345):
    std = 0
    x, y, z = 0, 0, 0
    for i in range(ACCUMULATED_NUMBER):
        axes = adxl345.getAxes(True)
        x_before, y_before, z_before = x, y, z
        x, y, z = axes['x'], axes['y'], axes['z']
        if i != 0:
            std += sqrt((x-x_before)**2 + (y-y_before)**2 + (z-z_before)**2)
        time.sleep(SLEEP_DELAY)
    if std > ON_OFF_STANDARD:
        print "- ON " + str(std)
        return True
    else:
        print "- OFF " + str(std)
        return False

def send_state(state):
    if state:
        print "* Send running_state"
        r = requests.get(URL+'id='+ID+'&state=run')
    else:
        print "* Send idle_state"
        r = requests.get(URL+'id='+ID+'&state=idle')

def change_beacon_state(state):
    if state:
        print "* Beacon_state running"
        msg = BLE_HEX_FIXED_FORWARD + BLE_HEX_MACHINE_ID + BLE_HEX_STATE_RUN + BLE_HEX_FIXED_BACK
        call(msg, shell=True)
    else:
        print "* Beacon_state idle"
        msg = BLE_HEX_FIXED_FORWARD + BLE_HEX_MACHINE_ID + BLE_HEX_STATE_IDLE + BLE_HEX_FIXED_BACK
        call(msg, shell=True)

if __name__ == "__main__":
    adxl345 = ADXL345()
    is_running = False
    count = 0

    Popen(['./scripts/init.sh'], shell=True)
    send_state(is_running)
    change_beacon_state(is_running)

    while True:
        if check_onoff(adxl345):
            if count < ACCUMULATED_STANDARD*2:
                count += 1
            if not is_running and count > ACCUMULATED_STANDARD:
                is_running = True
                send_state(is_running)
                change_beacon_state(is_running)
        else:
            if count > 0:
                count -= 1
            if is_running and count < ACCUMULATED_STANDARD+1:
                is_running = False
                send_state(is_running)
                change_beacon_state(is_running)

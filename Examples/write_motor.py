"""read_altitude.py: Reboot your flight controller (Betaflight)

Copyright (C) 2020 Ricardo de Azambuja

This file is part of YAMSPy.

YAMSPy is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

YAMSPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with YAMSPy.  If not, see <https://www.gnu.org/licenses/>.

Acknowledgement:
This work was possible thanks to the financial support from IVADO.ca (postdoctoral scholarship 2019/2020).

Disclaimer (adapted from Wikipedia):
None of the authors, contributors, supervisors, administrators, employers, friends, family, vandals, or anyone else 
connected (or not) with this project, in any way whatsoever, can be made responsible for your use of the information (code) 
contained or linked from here.
"""
from yamspy import MSPy


#
# On Linux, your serial port will probably be something like
# /dev/ttyACM0 or /dev/ttyS0 or the same names with numbers different from 0
#
# On Windows, I would expect it to be 
# COM1 or COM2 or COM3...
#
# This library uses pyserial, so if you have more questions try to check its docs:
# https://pyserial.readthedocs.io/en/latest/shortintro.html
#
#
serial_port = "COM3"

with MSPy(device=serial_port, loglevel='DEBUG', baudrate=115200) as board:
    # Read info from the FC
    # Please, pay attention to the way it works:
    # 1. Message is sent: MSP_ALTITUDE without any payload (data=[])

    board.set_ARMING_DISABLE(armingDisabled=0, runawayTakeoffPreventionDisabled=0)

    # d = board.convert([1000, 1200, 1000, 1000, 1000, 1000, 1000])

    #m = board.send_RAW_msg(MSPy.MSPCodes['MSP_MOTOR'], data=d)

    board.send_RAW_MOTORS([1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000])

    # print(m)

    command_list = ['MSP_API_VERSION', 'MSP_FC_VARIANT', 'MSP_FC_VERSION', 'MSP_BUILD_INFO', 
                    'MSP_BOARD_INFO', 'MSP_UID', 'MSP_ACC_TRIM', 'MSP_NAME', 'MSP_STATUS', 'MSP_STATUS_EX',
                    'MSP_BATTERY_CONFIG', 'MSP_BATTERY_STATE', 'MSP_BOXNAMES']

    if board.INAV:
        command_list.append('MSPV2_INAV_ANALOG')
        command_list.append('MSP_VOLTAGE_METER_CONFIG')

    for msg in command_list: 
        if board.send_RAW_msg(MSPy.MSPCodes[msg], data=[]):
            dataHandler = board.receive_msg()
            board.process_recv_data(dataHandler)
    if board.INAV:
        cellCount = board.BATTERY_STATE['cellCount']
    else:
        cellCount = 0 # MSPV2_INAV_ANALOG is necessary
    # last_loop_time = time.time()
    # Send the RC channel values to the FC
    print(board.MOTOR_DATA)
        # board.process_MSP_MOTOR(d)

    #if board.send_RAW_msg(MSPy.MSPCodes['MSP_MOTOR'], data=d):
        
        # board.process_MSP_MOTOR(d)

        # 2. Response msg from the flight controller is received
        #dataHandler = board.receive_msg()
        # 3. The msg is parsed
        #board.process_recv_data(dataHandler)
        # 4. After the parser, the instance is populated.
        # In this example, SENSOR_DATA has its altitude value updated.
        # print(board.SENSOR_DATA['altitude'])

# For some msgs there are available specialized methods to read them faster:
# fast_read_altitude
# fast_read_imu
# fast_read_attitude
# fast_read_analog
# fast_msp_rc_cmd
#
# Notice they all start with "fast_" ;)

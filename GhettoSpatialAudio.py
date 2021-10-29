#!/usr/bin/env python3

"""
A python script to simulate spatial audio (2D LR channels) using spatial data streamed from the Galaxy Buds Pro.

Based on the work of:
@ThePBone
"""

# License: MIT
# Author: @JediRhymeTrix
# 10/28/2021
import time

import sys
import argparse

from utils import conversions, audio_interface

from BudsProHeadtracking import Headtracking


initial_yaw = None

volume = audio_interface.get_volume_obj()


def __main_callback(quaternion):
    # This parameter is a float list describing a raw quaternion (4D vector)
    # The values are ordered like this: x, y, z, w

    roll_pitch_yaw = conversions.to_roll_pitch_yaw(quaternion)

    print("roll={}, pitch={}, yaw={}".format(
        roll_pitch_yaw[0], roll_pitch_yaw[1], roll_pitch_yaw[2]))

    global initial_yaw, volume

    yaw = quaternion[1]

    if initial_yaw is None:
        initial_yaw = yaw
        print("Initial yaw: ", initial_yaw)

    yaw_diff = (((yaw - initial_yaw) / initial_yaw) * 100)
    if abs(yaw_diff) > 200:
        yaw_diff = 200 if yaw_diff > 0 else -200

    balance = int((yaw_diff + 200) / (400) * (65))

    print("yaw_diff: ", yaw_diff)
    print("balance: ", balance)

    volume.SetChannelVolumeLevel(0, -balance, None)
    volume.SetChannelVolumeLevel(0, balance, None)


def main():
    parser = argparse.ArgumentParser(
        description='Stream head-tracking data from the Galaxy Buds Pro')
    parser.add_argument('mac', metavar='mac-address', type=str, nargs='?', const='58:a6:39:5d:77:90', default='58:a6:39:5d:77:90',
                        help='MAC-Address of your Buds')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Print debug information")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="Trace Bluetooth serial traffic")
    args = parser.parse_args()
    args.mac = [args.mac] if type(args.mac) is not 'list' else args.mac

    try:
        Headtracking.stream(args, __main_callback)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()

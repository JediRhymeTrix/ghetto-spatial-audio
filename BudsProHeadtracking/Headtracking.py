#!/usr/bin/env python3

"""
A python script to stream head-tracking data from the Samsung Galaxy Buds Pro
"""

# License: MIT
# Author: @ThePBone
# 04/26/2021
import time

import bluetooth
import sys
import argparse

from .SpatialSensorManager import SpatialSensorManager


def __spatial_sensor_callback(quaternion):
    # This parameter is a float list describing a raw quaternion (4D vector)
    # The values are ordered like this: x, y, z, w
    print("x={}, y={}, z={}, w={}".format(
        quaternion[0], quaternion[1], quaternion[2], quaternion[3]))
    # Conversion examples (C#): https://github.com/ThePBone/GalaxyBudsClient/blob/master/GalaxyBudsClient/Utils/QuaternionExtensions.cs#L48


def stream(args, callback=__spatial_sensor_callback):
    verbose = args.verbose
    trace = args.trace

    if verbose:
        print(str(bluetooth.lookup_name(args.mac[0])))
        print("Searching for RFCOMM interface...")

    service_matches = bluetooth.find_service(
        uuid="00001101-0000-1000-8000-00805F9B34FB", address=str(args.mac[0]))

    port = host = None
    for match in service_matches:
        if match["name"] == "GEARMANAGER" or match["name"] == b"GEARMANAGER":
            port = match["port"]
            host = match["host"]
            break

    if port is None or host is None:
        print("Couldn't find the proprietary RFCOMM service")
        sys.exit(1)

    if verbose:
        print("RFCOMM interface found. Establishing connection...")

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))

    if verbose:
        print("Connected to device.")

    sensor = None
    try:
        sensor = SpatialSensorManager(
            sock, callback, verbose, trace)
        sensor.attach()

        while True:
            time.sleep(1000)

    except KeyboardInterrupt:
        if sensor is not None:
            sensor.detach()

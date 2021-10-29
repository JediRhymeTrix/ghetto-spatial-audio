import math


def to_roll_pitch_yaw(quarternion):
    result = [0.0, 0.0, 0.0]

    q = quarternion

    # roll
    result[0] = float(math.atan2(2.0 * (q[2] * q[1] + q[3] * q[0]),
                      1.0 - 2.0 * (q[0] * q[0] + q[1] * q[1])))
    # pitch
    result[1] = float(math.asin(2.0 * (q[1] * q[3] - q[2] * q[0])))
    # yaw
    result[2] = float(math.atan2(
        2.0 * (q[2] * q[3] + q[0] * q[1]), - 1.0 + 2.0 * (q[3] * q[3] + q[0] * q[0])))

    return result

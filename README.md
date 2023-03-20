# [WIP] Ghetto Spatial Audio

Uses real-time head tracking data from the Galaxy Buds Pro to simulate spatial audio in a quick and dirty way by manipulating the left and right channel balance in the audio output.

**Compatible with Windows ONLY**

## Requirements

- **Galaxy Buds Pro**
- **Python 3.5 (library constraints)**

## Instructions

Run \
**`pip install -r requirements.txt`** \
Find the MAC address of your Galaxy Buds Pro and run \
**`python GhettoSpatialAudio.py <MAC_ADDRESS>`** \
For additional options, run \
**`python GhettoSpatialAudio.py --help`**

Credits to [ThePBone](https://github.com/ThePBone/BudsPro-Headtracking)

#### NOTE: This project is currenty dead in the water as Windows no longer allows changing volume for individual channels on the Galaxy Buds Pro

#!/usr/bin/env python3
# 
# Desk Buddy by Robert Kight, Copyright 2020.
#
# This is a little helper program for minimal environments based around window managers like dwm, spectrwm, i3wm, etc. Such setups usually don't rely on background programs to manage things like screen brightness and audio volume levels. The point of this program is to keep users from cluttering up their configuration files with long and hacky commands. Put them here instead and use the convenience functions in your WM config file.
#
# Currently implemented features:
#
# - Use 'xrandr' to change the fucking brightness.
# - Use 'amixer' to change the volume.

import os
import sys
import json
from pathlib import Path

# Get the path to the brightness file.
configFile = str(os.path.join(Path.home(), '.deskbuddyrc'))

# Create the config file if it doesn't exist.
def createConfig():
    print("Unable to read config file '.deskbuddyrc'.")
    print("Attempting to create the file...")

    # Default settings dict
    settings = {
        'brightness': 10,
        'volume': 50,
        'mute': False
    }
    writeConfig(settings)

    print("Success!")
    sys.exit()

# Get the current brightness from '.brightness' file in the home 
# directory.
def readConfig():

    # Try to read the file
    try:
        with open(configFile) as f:
            contents = f.read()
            settingsDict = json.loads(contents)

        # Return the file contents
        return settingsDict

    # If the file does not exist, try to creat it.
    # except (FileNotFoundError, ValueError) as e:
    #except FileNotFoundError:
    except:
        createConfig()


# Write the settings to a file.
def writeConfig(settings):
    with open(configFile, 'w') as f:

        # Convert the setting dictionary to a JSON.
        jsonSettings = json.dumps(settings)
        f.write(jsonSettings)


# Run the necessary command to set brightness.
# Lowers brightness by default.
def setBrightness(brightUp=False, amount=1):

    # Get current settings.
    currentSettings = readConfig()

    # Extract the current brightness level.
    brightness = currentSettings['brightness']

    # Modify brightness.
    if brightUp:
        brightness += 1
    else:
        brightness -= 1
        
    # Update the file with the new value.
    currentSettings['brightness'] = brightness
    writeConfig(currentSettings)

    # 'xrandr' expects a floating point value between 0.0 and 1.0.
    # Let's make sure that we don't pass an invalid value
    if brightness > 0 and brightness < 11:


        cmd = 'xrandr --output eDP-1 --brightness {}'.format(brightness * 0.1)
        os.system(cmd)


# Use amixer to set the volume.
# Volume is set as a percentage, so an integer between 1 and 100.
def setVolume(volUp=False, amount=5):
    
    # Get current settings.
    currentSettings = readConfig()

    # Extract the current volume level.
    vol = currentSettings['volume']

    if volUp:
        vol += amount
    else:
        vol -= amount
    
    # Update the file
    currentSettings['volume'] = vol
    writeConfig(currentSettings)

    # Validate the volume for lowering or raising.
    if vol > -1 and vol < 101:

        cmd = "amixer set Master {}%".format(vol)
        os.system(cmd)


def setMute():
    # Get current settings.
    currentSettings = readConfig()

    # Extract the current volume level.
    mute = currentSettings['mute']

    if mute:
        cmd = "amixer set Master unmute"
        os.system(cmd)
        mute = False

    else:
        cmd = "amixer set Master mute"
        os.system(cmd)
        mute = True
        

    # Update the file
    currentSettings['mute'] = mute
    writeConfig(currentSettings)


def main():
    # print(configFile)
    # print(readCurrentBrightness())
    help_message = """
Desk Buddy v0.0.1, Copyright 2020 Robert Kight
License: MIT

Valid commands:
bright_up   - Increase brightness
bright_down - Decrease brightness
volume_up   - Increase volume
volume_down - Decrease volume
mute        - Toggle audio mute
    """

    # Make sure that we have a valid command to work with.
    if len(sys.argv) > 1:
        #print(sys.argv[1])
        if sys.argv[1] == 'bright_up':
            setBrightness(True)
        elif sys.argv[1] == 'bright_down':
            setBrightness()
        elif sys.argv[1] == 'volume_up':
            setVolume(True)
        elif sys.argv[1] == 'volume_down':
            setVolume()
        elif sys.argv[1] == 'mute':
            setMute()
        else:
            print(help_message)
    else:
        print(help_message)


if __name__ == "__main__":
    main()

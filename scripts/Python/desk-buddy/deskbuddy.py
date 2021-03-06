#!/usr/bin/env python3
# 
# Desk Buddy by Robert Kight, Copyright 2020.
#
# This is a little helper program for minimal environments based around
# window managers like dwm, spectrwm, i3wm, etc. Such setups usually don't
# rely on background programs to manage things like screen brightness and
# audio volume levels. The point of this program is to keep users from
# cluttering up their configuration files with long and hacky commands.
# Put them here instead and use the convenience functions in your WM config
# file.
#
# Currently implemented features:
#
# - Use 'xrandr' to change the brightness (software only, does not control
# screen backlight.
# - Use 'amixer' to change the volume.
#
# NOTE: When trying to set hardware brightness, it looks inside
# /sys/class/backlight. If that directory does not exist, please consult
# the documentation of your chosen Linux/BSD distribution to figure out where
# the brightness and max_brightness files are.
# File permissions are another problem. Sometimes the files that need to be
# modified are locked behind root permissions. Again, consult the
# documentation to figure out the "proper" way to change these files.

import os
import sys
import json
from pathlib import Path

# Get the path to the brightness file.
configFile = str(os.path.join(Path.home(), '.deskbuddyrc'))

# Create a settings file with default data.
def createConfig(configFile):
    print("Unable to read config file '.deskbuddyrc'.")
    print("Attempting to create the file...")

    # Default settings dict
    settings = {
        'softBrightness': 10,
        'softBrightnessStep': 1,
        'hardBrightness': 50,
        'hardBrightnessStep': 10,
        'volume': 50,
        'volumeStep': 5,
        'mute': False,
        'hardBrightnessEnabled': False,
        'sessionDefaults': {
            'softBrightness': 10,
            'hardBrightness': 50,
            'volume': 50,
            'mute': False,
            'hardBrightnessEnabled': False
        }
    }
    writeConfig(settings, configFile)

    print("Success!")
    sys.exit()


# Read and parse the settings file.
def readConfig(configFile):

    # Try to read the file.
    try:
        with open(configFile) as f:
            contents = f.read()
            settingsDict = json.loads(contents)

        # Return the file contents.
        return settingsDict

    # If the file does not exist, try to create it.
    # except (FileNotFoundError, ValueError) as e:
    #except FileNotFoundError:
    except:
        createConfig(configFile)
        return False


# Write the settings to a file.
def writeConfig(settings, configFile):
    with open(configFile, 'w') as f:

        # Convert the setting dictionary to a JSON.
        jsonSettings = json.dumps(settings, sort_keys=False, indent=4)
        f.write(jsonSettings)


# Run the necessary command to set brightness.
# Lowers brightness by default.
# Defaults the 'xrandr' for setting SOFTWARE brightness.

# Set HARDWARE screen brightness with xbacklight.
def setBrightnessXbacklight(brightVal, currentSettings):

    # Get the brightness step value.
    # Defaults to 10.

    stepValue = 10
    if 'hardBrightnessStep' in currentSettings.keys():
        stepValue = currentSettings['hardBrightnessStep']

    # Extract the current brightness level.
    brightness = currentSettings['hardBrightness']

    # Modify brightness.
    if brightVal == 'up':
        brightness += stepValue
    elif brightVal == 'down':
        brightness -= stepValue
    else:
        brightness = int(brightVal)
        
    # 'xbacklight' expects an integer between 10 and 100.
    # Let's make sure that we don't pass an invalid value.
    if brightness > 0 and brightness < 101:


        cmd = 'xbacklight -set {}%'.format(brightness)
        os.system(cmd)
    
        # Update the file with the new value.
        currentSettings['hardBrightness'] = brightness

        
    return currentSettings


# Set SOFTWARE screen brightness with xrandr.
def setBrightnessXrandr(brightVal, currentSettings):
   
    # First, check 'hardBrightnessEnabled'. If true, run the
    # Xbacklight function instead.
    if currentSettings['hardBrightnessEnabled']:
        currentSettings = setBrightnessXbacklight(brightVal, currentSettings)
    else:

        # Get the brightness step value.
        # Defaults to 1.

        stepValue = 1
        if 'softBrightnessStep' in currentSettings.keys():
            stepValue = currentSettings['softBrightnessStep']

        # Extract the current brightness level.
        brightness = currentSettings['softBrightness']

        # Modify brightness.
        if brightVal == 'up':
            brightness += stepValue
        elif brightVal == 'down':
            brightness -= stepValue
        else:
            brightness = int(brightVal)
            
        # 'xrandr' expects a floating point value between 0.0 and 1.0.
        # Let's make sure that we don't pass an invalid value.
        if brightness > 0 and brightness < 11:

            # Update the file with the new value.
            currentSettings['softBrightness'] = brightness

            cmd = 'xrandr --output eDP1 --brightness {}'.format(brightness * 0.1)
            os.system(cmd)

    return currentSettings


# Use amixer to set the volume.
# Volume is set as a percentage, so an integer between 1 and 100.
def setVolume(soundVal, currentSettings):
    
    # Extract the current volume level.
    vol = currentSettings['volume']

    # Get the volume step.
    # Defaults = 5.

    stepValue = 5
    if 'volumeStep' in currentSettings.keys():
        stepValue = currentSettings['volumeStep']
        

    if soundVal == 'up':
        vol += stepValue
    elif soundVal == 'down':
        vol -= stepValue
    else:
        vol = int(soundVal)
    
    # Validate the volume for lowering or raising.
    if vol > -1 and vol < 101:

        cmd = "amixer set Master {}%".format(vol)
        os.system(cmd)
        
        # Update the file.
        currentSettings['volume'] = vol


    return currentSettings
    

def setMute(action, currentSettings):
  
    cmd = 'amixer set Master'
    if action == 'toggle':
        # Extract the current volume level.
        mute = currentSettings['mute']

        if mute:
            cmd += ' unmute'
            mute = False

        else:
            cmd += ' mute'
            mute = True

    elif action == 'mute':
        cmd += ' mute'
        mute = True
    
    elif action == 'unmute':
        cmd += ' unmute'
        mute = True

   
    # Run the command.
    os.system(cmd)
        

    # Update the file.
    currentSettings['mute'] = mute

    return currentSettings


# Read all default settings and restore the values.
def restoreDefaults(currentSettings):
    defaults = currentSettings['sessionDefaults']

    # Brightness.
    if defaults['hardBrightnessEnabled']:
        b = defaults['hardBrightness']
        currentSettings = setBrightnessXbacklight(b, currentSettings)
    else:
        b = defaults['softBrightness']
        currentSettings = setBrightnessXrandr(b, currentSettings)

    # Audio
    v = defaults['volume']
    currentSettings = setVolume(v, currentSettings)

    if defaults['mute']:
        currentSettings = setMute('mute', currentSettings)
    else:
        currentSettings = setMute('unmute', currentSettings)

    return currentSettings


def main():
    help_message = """
Desk Buddy v0.0.1, Copyright 2020 Robert Kight
License: MIT

Valid commands:
bright_up   - Increase brightness
bright_down - Decrease brightness
volume_up   - Increase volume
volume_down - Decrease volume
mute        - Toggle audio mute
restore     - Restore default audio and brightness levels
    """

    # Read the current config and pass it to each of the command function.
    # The 'if' statement is here to make sure that nothing runs if the
    # config file doesn't exist.
    currentSettings = readConfig(configFile)
    if currentSettings:

        # Make sure that we have a valid command to work with.
        if len(sys.argv) > 1:
            #print(sys.argv[1])
            if sys.argv[1] == 'bright_up':
                currentSettings = setBrightnessXrandr('up', currentSettings)
            elif sys.argv[1] == 'bright_down':
                currentSettings = setBrightnessXrandr('down', currentSettings)
            elif sys.argv[1] == 'volume_up':
                currentSettings = setVolume('up', currentSettings)
            elif sys.argv[1] == 'volume_down':
                currentSettings = setVolume('down', currentSettings)
            elif sys.argv[1] == 'mute':
                currentSettings = setMute('toggle', currentSettings)
            elif sys.argv[1] == 'restore':
                currentSettings = restoreDefaults(currentSettings)
            else:
                print(help_message)
        else:
            print(help_message)

        # Update the settings.
        writeConfig(currentSettings, configFile)


if __name__ == "__main__":
    main()

# Desk Buddy

This python program helps take the hassel out of getting volume and brightness keys to work on laptops. The goal is to provide a program that people can just download and plug directly into the key bindings of their chosen window manager. It will automatically figure out the right commands to adjust volume and display brightness on most laptops.


## Features

- Dim or brighten the screen in software (via `xgamma`) or hardware (via `xbacklight`)
- Raise, lower, and mute master volume (via ALSA or PulseAudio)

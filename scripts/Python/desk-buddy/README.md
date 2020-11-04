# Desk Buddy

This python program helps take the hassel out of getting volume and brightness keys to work on laptops. The goal is to provide a program that people can just download and plug directly into the key bindings of their chosen window manager. Once complete, it will automatically figure out the right commands to adjust volume and screen brightness on most laptops.


## What it can do right now

- Dim or brighten the screen with `xrandr` or `xbacklight` commands
- Raise, lower, and mute master volume with `amixer`


## Screen brightness adjustment

### Software only

The method with `xrandr` is the *safe* method. The brightness of the screen is modified with *software*. The physical hardware backlight is not affected. This is the recommended option for users who don't want to modify system files. It's also the default option.


### Hardware, easy mode

If you want "true" backlight adjustment, first check if the program `xbacklight` will work on your system. Depending on your chosen distribution, you may need to modify the permissions of files under `/sys/class/backlight/<manufacturer>` and/or put the following in your `/etc/X11/xorg.conf` file:

``` shell
Section "Device"
    Identifier  "Intel Graphics" 
    Driver      "intel"
    Option      "Backlight"  "intel_backlight"
EndSection<Paste>
```

**Please keep in mind that this program was only tested on a laptop with Intel graphics. If your laptop has non-Intel graphics (Nvida, Radeon, etc), the above snippet will need to be modified.**


Once you get `xbacklight` to work, make sure you set "hwbr" to "true". `.deskbuddyrc`


### Hardware, hard mode

This requires direct modification of the program to correctly read and manipulate the files under `/sys/class/backlight`. If you want to go this route, you're on your own.



## Tested on

- Debian 10.6 x86\_64 with Intel graphics

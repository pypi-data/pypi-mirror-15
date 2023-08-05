extended Brightness
===================

Copyright Jörg Mäder - 2016-05-05 - Version 1.0.4 - http://www.toolcase.org/app/linux/extBrightness

This tool allows to control brightness and gamma for all connected
screens on a X11 system (which is the case for the most linux systems).
extBrightness can be used using the terminal or the implemented GUI.

**HINT**: This tool is a software solution and works additional to the 
hardware settings of your screens. The hardware settings will not be changed!
(I simply don't know how)



Command line options
--------------------

  -h, --help            show this help message and exit
  -b NUM                set brightness (float between 0.0 - 1.999 or integer
                        between 2 - 200)
  -B NUM                set brightness by increment. Hint: To small changes
                        may not work
  -c, --count           count the connected screens
  -d DISPLAY            Limit action to this Screen. Use 'a' for all, 'p' for
                        primary and 'np' for non-primary
  -g GAMMA              set gamma correction. Either one or three float values
                        between 0 and 10 separated by ':'
  -l                    list screens, together with '-v' the current values
                        are shown.
  -p                    show key of primary screen, use -v for more details
  -r                    reset (set brightness to 100% and gamma to 1)
  -t TEMP               set gamma using a temperature in Kelvin
  -u                    undo last changes (saved in profile [last])
  -D                    set the brightness to 0 or to the last value if it is
                        already 0
  -v                    verbose output including the ``xrandr`` command which
                        was used to set the new values.
  --gui                 show user interface after processing the other options
                        (default if no option is present)
  --version             show current version
  --hard                Apply changes using ``xrandr`` even nothing has changed
  --virtual             do not apply changes but show potential results
  --file FILE           file used for saving profiles and other settings
                        (default: ~/.extBrightness.xml)
  -P NAME, --profile-load NAME
                        load profile
  --profile-save NAME   save current values as profile. If option --gui is
                        used too, the final values of it will be saved!
  --profile-delete NAME
                        delete profile
  --profile-show NAME   show profile
  --profile-list        list all profiles. Use '-v' too for displaying the
                        saved values.


Tips
----

This program may set all your screens to complete darkness (brightness = 0). For such a situation it is a good idea
to have a key binding on your system to the gui of extBrightness. After it is started you just have to hit *[r]*
and  all screens are set to 100% brightness and gamma 1.

If you use option ``--profile-save NAME`` and ``--gui`` together, the final values from the gui
are saved to the profile *NAME*.

With ``extBrightness -d np -D`` you can switch all external screens *off* and *on* again. Please check before, 
if one of your screens is set as primary! If you are not sure use ``extBrightness -p``. If the output is empty, 
you have to define a screen as primary first (typically using your OS settings > screens > select one > set primary).  

The values applied (by ``xrandr``) to your system are not necessary exactly the same as you use in the options. Therefore small
changes may not have always an effect. Of course, you can bidn this command to a key using your OS to make it even more easy.





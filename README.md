# How to Use

To use this, download the source code zip and open the file called "index.html" with your browser.

The automation ability only works in Chromium based browsers, with the spoiler enabled, and if things are in the default windows places. If you want to try getting the auto tracker to work under other conditions, feel free to ask for help.

Probably compatible with Randomizer Mod versions 3.0.2 and 3.1.0.

This webpage behaves the same as the original entrance tracker except it has two new buttons in settings:

![A screen cap of the new settings menu with the two new buttons "pick file" and "stop watching" higlighted in red. the new buttons are between the Reset Tracker buttn and smooth images checkbox ](settings_menu.PNG)

Pick File: Choose the Tunic file that is created by the auto tracking script located at

```
USER_NAME\\Documents\\2024-1-31_12.50.50_tunic-tracker.txt
```

When this file updates, so will the tracker.

Stop Watching: Stop watching the save file so updates are no longer automatic.

The auto tracker scripts is a python file located at

`auto_tracker/auto_tracker.py`

Open the folder that contains index.html in the command line and run

```
python auto_tracker/auto_tracker.py
```

This will require Python 3.10+ to run: https://www.python.org/downloads/

When installing Python, make sure to click the option to add python.exe to the PATH.

![The python isntall menu with the add to path option highlighted and selected](python.PNG)


# Original Tunic Entrance Tracker

This is mostly a copy of Scipio's Tunic Entrance Tracker https://scipiowright.gitlab.io/tunic-tracker/

Here is a link to the original, which Scipio's is forked off of:
https://sekii.gitlab.io/pokemon-tracker

## License
The code is under the [MIT License](code/LICENSE.txt). Original code by Sekii.

Data, fonts, and images belong to their own copyright holders.

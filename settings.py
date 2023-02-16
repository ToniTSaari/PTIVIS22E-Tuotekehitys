'''
Handles game settings.

Call `settings.init()` before trying to do anything else with the module,
for example at the very start of the game.

The module contains the following variables for accessing different settings
or groups of settings:

all - All currently loaded settings in a dict.

display - Settings related to the game window in a dict.
'''
import json


all = None
display = None
ambientm = None
sfxm = None

def init() -> None:
    '''
    Read game settings from a file and set module variables for easy access.

    Should be called before any settings are accessed, so usually at the start
    of the game. See the module documentation for further information about
    the access variables.

    Raises an exception if settings.json cannot be read for any reason.
    '''
    with open('settings.json', 'r') as file:
        global all, display, ambientm, sfxm
        data = file.read()
        all = json.loads(data)
        display = all["display"]
        ambientm = all["ambientm"]
        sfxm = all["sfxm"]

def write(data) -> None:
    with open('settings.json', 'w') as file:
        save = json.dumps(data, indent=4)
        file.write(save)

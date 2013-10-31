from pprint import pprint as p
# optional, will allow Up/Down/History in the console
import readline

import code

from navigate import *

vars = globals().copy()
vars.update(locals())
shell = code.InteractiveConsole(vars)
shell.interact()

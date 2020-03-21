# Take a set of bit strings and convert the 'x's (don't knows) into either
# ones or zeros depending on options.
# -1: convert to ones, -0 convert to zeros

from sys import argv

# default value to change'x's into
DEFAULT_OPT = "1"

def argument_opt(args):
    """returns the option to change xs into"""
    if len(args) > 1:
        if args[1] == "-1":
            return "1"
        elif args[1] == "-0":
            return "0"
    return DEFAULT_OPT

replace_opt = argument_opt(argv)

# filename 
FILE = "copy_across.txt"

lines = []
with open(FILE, "r") as f:
    lines = f.read()

lines = lines.replace("x", replace_opt)

with open(FILE, "w") as f:
    f.write(lines)

from SevenSeg import SevenSeg
from Board import Board

"""These two characters let us have alternate ways of passing information from the file.
   *IGNORE_CHAR will ignore the line: this is because ModelSim outputs lines starting 
    with # so by leaving the output untouched it'll be skipped here.
   *CAPTION_CHAR will designate the line to be printed straight into the output, between
    Board prints. Useful for annotating things like 'button pressed'."""
IGNORE_CHAR  = '#'
CAPTION_CHAR = '@'
#COMMAND_CHAR = '\'

def main(fname, invert=True):
    # get all of the lines of bitstrings from the file
    lines = []
    with open(fname, "r") as f:
        lines = f.read()

    # go through each line, determine if it is for display, caption or to be skipped.
    for line in lines.split('\n')[:-1]:     #[:-1] to skip the stripped trailing \n
        
        print()

        if line[0] == IGNORE_CHAR: continue
        elif line[0] == CAPTION_CHAR:
            print(line[1:])
        else:
            b = Board(line.split(" "), invert)
            print(b)

def str2bool(string):
    """Take a string and return if it represents True or False. Errors are returned False"""
    if string == "True": return True
    elif string == "False": return False
    return False

if __name__ == "__main__":
    from sys import argv
    # 2 args: just the filename, 3 args: also invert flag. Need to have a str->bool conversion here
    if len(argv) == 2:
        main(argv[1])
    elif len(argv) == 3:
        main(argv[1], str2bool(argv[2]))
    else:
        print("usage: python3 script filename [invert]\ninvert is True or False (default True)")

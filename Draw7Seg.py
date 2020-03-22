# Render a binary string to what it would look like on an Altera Development
# Board, rendering 6 seven segment displays and 10 LEDs. 
# Uses the MSB convention of Verilog: [6:0] indicates that the leftmost bit is the MSB
# From MSB to LSB:
#
#    +--0--+
#    |     |
#    5     1
#    |     |
#    +--6--+
#    |     |
#    4     2
#    |     |
#    +--3--+
#
#
# Note: Be careful about what you stick in as input, I wasn't __super__ thorough
# with the input verification, as I'm generating input through verilog/ModelSim
# Also, the invert flag seems not to work but atm I don't really care
#
# Alexander Leris 12/3/20

from copy import deepcopy

class SevenSeg():
    def __init__(self, bits, invert=True):
        if len(bits) != 7:
            raise ValueError("length of bitstring must be 7")

        if invert:
            self.bits = SevenSeg.invert(bits)
        else:
            self.bits = bits
        
        self.grid = self.make_grid()

    def __str__(self):
        out = ""
        for row in self.grid:
            out += ''.join(row) + "\n"
        return out
        
    def get_grid(self):
        return deepcopy(self.grid)

    def make_grid(self):
        """
        create a 2d list representation of the number
        """

        s = SevenSeg.str_reverse(self.bits)
        # we can now refer to the using the same indicies as verilog and the pins
        # (started with python numbering [0,1,2,3,4,5,6] now having verilog [6,5,4,3,2,1,0]

        # intialise empty grid
        grid = [['.', '.', '.', '.', '.', '.', '.'],
                ['.', ' ', ' ', ' ', ' ', ' ', '.'],
                ['.', ' ', ' ', ' ', ' ', ' ', '.'],
                ['.', ' ', ' ', ' ', ' ', ' ', '.'],
                ['.', '.', '.', '.', '.', '.', '.'],
                ['.', ' ', ' ', ' ', ' ', ' ', '.'],
                ['.', ' ', ' ', ' ', ' ', ' ', '.'],
                ['.', ' ', ' ', ' ', ' ', ' ', '.'],
                ['.', '.', '.', '.', '.', '.', '.']]

        # go through the "truth table", assigning sections of the grid based on the indicies (top of code)
        if s[0] == '1':
            # write the whole top row as 1s
            grid[0] = ['#' for i in range(7)]
        if s[1] == '1':
            for i in range(5):
                grid[i][6] = '#'
        if s[2] == '1':
            for i in range(5):
                grid[i+4][6] = '#'
        if s[3] == '1':
            grid[8] = ['#' for i in range(7)]
        if s[4] == '1':
            for i in range(5):
                grid[i+4][0] = '#'
        if s[5] == '1':
            for i in range(5):
                grid[i][0] = '#'
        if s[6] == '1':
            grid[4] = ['#' for i in range(7)]

        return grid

    def invert(bits):
        out = ""
        for char in bits:
            if char == '1':
                out += '0'
            elif char == '0':
                out += '1'
            else:
                raise ValueError("invalid bit string ({}). Must contain only '0' and '1'".format(bits))
        return out
    
    def str_reverse(s):
        return s[::-1]


class Board():
    """Board will read in a series of ' '-delimited bitstrings to be interpreted
    as 6 seven segment display inputs and 10 LED inputs, and can print them out 
    to mimic the Altera Development Board.
    """
    NUM_7SEG = 6    # MUST BE > 1. Should never change though
    
    def __init__(self, data_list, invert=True):
        """Takes in a list containing the strings. the format is
            6 * 7'bxxxxxxx, 10'bxxxxxxxxxx
            Data integrity won't be checked here for the time being!
        """
        # assume data is correctly formatted
        
        # get the bitstrings
        self.hex_strings = data_list[0:self.NUM_7SEG]
#         self.leds = data_list[-1][::-1]         # reverse order to match verilog
        self.leds = data_list[-1]
        
        # convert hex_strings into display_grid forms
        # don't catch any value errors, that's not our job
        self.hex_grids = [SevenSeg(hex_string, invert).get_grid() for hex_string in self.hex_strings]
        
        # initialise display grid
        self.display_grid = self.hexes_2_display_grid()
        
        
    def hexes_2_display_grid(self):    
                
        if self.hex_grids[0]:
            self.display_grid = deepcopy(self.hex_grids[0])
            
            if len(self.hex_grids) > 1:
                # add the rest of the hexes row by row along the side of this one   
                for hex in self.hex_grids[1:]:
                    for i in range(len(hex)):
                        self.display_grid[i].extend(' ')
                        self.display_grid[i].extend(hex[i])
                
        else:
            # this shouldn't happen, it would mean that no strings were read in?
            raise ValueError("couldn't work with hex:\n{}".format(repr(self.hex_grids[0])))
            
        return self.display_grid
    
    def __str__(self):
        out = ""
        # HEXes
        for row in self.display_grid:
            out += ''.join(row) + '\n'
        
        # LEDRs
        out += '\n'
        # print a line with the LED numbering
        for i in range(len(self.leds)):
            out += " {}  ".format(len(self.leds) -i -1)
            
        # print out "icons" for the leds. buffer let's us repeat this multiple times
        buffer = ""
        for i in range(len(self.leds)):
            if self.leds[i] == '1':
                buffer += "### "
            else:
                buffer += "... "
        out += ('\n' + buffer) * 3
        return out
        
    def other2string(self):
        """alternate implementation of __str__(). doesn't do the LEDs"""
        out = ""
        for i in range(len(self.hex_grids[0])):
            for j in range(len(self.hex_grids)):
                # add leading space for all non-leading hexes
                if j != 0:
                    out += ' '
                out += ''.join(self.hex_grids[j][i])
            out += '\n'
        return out
            

def main(fname, invert=True):
    lines = []
    with open(fname, "r") as f:
        lines = f.read()

    for line in lines.split('\n')[:-1]:     #[:-1] to skip the stripped trailing \n
        
        b = Board(line.split(" "), invert)
        print()
        print(b)

if __name__ == "__main__":
    from sys import argv
    if len(argv) == 2:
        main(argv[1])
    elif len(argv) == 3:
        main(argv[1], argv[2])
    else:
        print("usage: python3 script filename [invert]\ninvert is True or False (default True)")

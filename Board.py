
#
# Alexander Leris 12/3/20

from SevenSeg import SevenSeg
from copy import deepcopy

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
            
        # print out "icons" for the leds. buffer let's us repeat this for 3 rows
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

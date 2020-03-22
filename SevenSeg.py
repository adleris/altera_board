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


from copy import deepcopy

class SevenSeg():
    def __init__(self, bits, invert=True):
        if len(bits) != 7:
            raise ValueError("length of bitstring must be 7")

        if invert:
            self.bits = invert_bitstring(bits)
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

        s = str_reverse(self.bits)
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

def invert_bitstring(bits):
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

from SevenSeg import SevenSeg
from Board import Board

def main(fname, invert=True):
    # get all of the lines of bitstrings from the file
    lines = []
    with open(fname, "r") as f:
        lines = f.read()

    for line in lines.split('\n')[:-1]:     #[:-1] to skip the stripped trailing \n
        
        b = Board(line.split(" "), invert)
        print()
        print(b)

if __name__ == "__main__":
    from sys import argv
    # 2 args: just the filename, 3 args: also invert flag. Need to have a str->bool conversion here
    if len(argv) == 2:
        main(argv[1])
    elif len(argv) == 3:
        main(argv[1], argv[2])
    else:
        print("usage: python3 script filename [invert]\ninvert is True or False (default True)")

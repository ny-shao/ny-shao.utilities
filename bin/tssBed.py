#! /usr/bin/env python

import argparse
import sys
import string

def getPIPEBED():
    temp_list = []
    while True:
        next_line = sys.stdin.readline()
        if not next_line:
            break
        next_line = string.strip(next_line)
        temp_list.append(next_line)
    return temp_list

def getFileBED(fileName):
    return [string.strip(x) for x in open(fileName, 'r')]

def getNewLine(input_line, v):
    in_lineL = input_line.strip().split("\t")
    ## extract TSS
    if v == False:
        if in_lineL[6] == "+":
            in_lineL.append(in_lineL[1])
            in_lineL.append(in_lineL[2])
            in_lineL[2] = str(int(in_lineL[1]) + 1)
        else:
            in_lineL.append(in_lineL[1])
            in_lineL.append(in_lineL[2])
            in_lineL[1] = str(int(in_lineL[2]) - 1)
    else:
        if in_lineL[6] == "+":
            in_lineL.append(in_lineL[1])
            in_lineL.append(in_lineL[2])
            in_lineL[1] = str(int(in_lineL[2]) - 1)
        else:
            in_lineL.append(in_lineL[1])
            in_lineL.append(in_lineL[2])
            in_lineL[2] = str(int(in_lineL[1]) - 1)
    new_line = "\t".join(in_lineL)
    return new_line

def main():
    parser = argparse.ArgumentParser(
        description='Generate TSS (or TES with -v) of BED, the original info of genebody attached to the right-most.')
    parser.add_argument('-i', help='Input BED. Default from stdin.', required=True, default="-")
    parser.add_argument('-v', help='To generate TES, not TSS.', action='store_true', default=False)
    args = vars(parser.parse_args())
    if args['i'] == "-":
        BED_lines = getPIPEBED()
    else:
        BED_lines = getFileBED(args['i'])
    new_BED_lines = [getNewLine(x, args['v']) for x in BED_lines]
    print "\n".join(new_BED_lines)

if __name__ == '__main__':
    main()
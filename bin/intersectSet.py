#! /usr/bin/env python

import os
import argparse
import sys
import subprocess
import string

def getPIPESet():
    temp_list = []
    while True:
        next_line = sys.stdin.readline()
        if not next_line:
            break
        next_line = string.strip(next_line)
        temp_list.append(next_line)
    return set(temp_list)

def getFileSet(fileName):
    return set(string.strip(x) for x in open(fileName, 'r'))


def main():
    parser = argparse.ArgumentParser(description='Mimic of bedtools to manipulate gene list set')
    parser.add_argument('-a', help='SetA', required=True, default="-")
    parser.add_argument('-b', help='SetB', required=True, default="-")
    parser.add_argument('-v', help='specific of setA', action='store_true', default=False)
    args = vars(parser.parse_args())
    assert (args['a'], args['b']) != ('-', '-')
    if args['a'] == '-':
        setA = getPIPESet()
    else:
        setA = getFileSet(args['a'])
    if args['b'] == '-':
        setB =getPIPESet
    else:
        setB = getFileSet(args['b'])

    if args['v'] == False:
        res = {x for x in setA if x in setB}
    else:
        res = {x for x in setA if x not in setB}

    for x in res:
        sys.stdout.write(x+"\n")
    sys.stdout.flush()

    

if __name__ == '__main__':
    main()
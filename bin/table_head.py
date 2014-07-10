#!/usr/bin/env python
#  Author: Ning-Yi SHAO shaoningyi@gmail.com
# -*- coding: utf-8 -*-

"""
table_head.py

TODO
Color of | and header?

"""
__date__ = '2012-06-01 16:59:54'

import os
import sys
import string
import commands
from optparse import OptionParser

def transpose(matrix):
    return  map(list, zip(*matrix))

def get_terminal_width_resize():
    """
    use 'tput cols' to fetch the width of the terminal.
    """
    c = commands.getoutput('tput cols').split('\n')[0]
    if c:
        return int(c)
    else:
        return None

def split_matrix(lines_matrix, i):
    a = transpose(lines_matrix)
    b = a[:i]
    c = a[i:]
    return (transpose(b), transpose(c))

def print_matrix(max_cell, lines_matrix, terminal_w):
    len_i = [sum(max_cell[:i+1]) for i in range(len(max_cell))]
    lines_matrix_next = None
    for i in range(len(len_i)):
        if terminal_w < (len_i[i]+i):
            # split the lines_matrix
            (lines_matrix, lines_matrix_next) = split_matrix(lines_matrix, i)
            break
    for line in lines_matrix:
        print '|'.join([ s.ljust(w) for w,s in zip(max_cell, line)])
    if lines_matrix_next != None:
        print '-'*terminal_w
        print_matrix(max_cell[i:], lines_matrix_next, terminal_w)

def main():
    opt_parser =  OptionParser()
    opt_parser.add_option('-l', '--lines', action='store',
    dest='line_no', help='header lines to be printed.', default='1')
    opt_parser.add_option('-d', '--direction', action='store',
    dest='direction', help='direction of printing. v or h.',
    default='h')
    opt_parser.add_option('-t', '--tab', action='store',
    dest='tab_word', help='tab word. s or t. s: space. t: tab.', default='t')
    (options, args) = opt_parser.parse_args(sys.argv)
    
    in_f = file(args[1])
    lines = []
    i = 0
    while i < int(options.line_no):
        line = in_f.readline()
        if len(line) == 0:
            break;
        line = string.strip(line)
        if options.tab_word=='t':
            lineL = string.split(line, sep='\t')
        elif options.tab_word=='s':
            lineL = string.split(line, sep=' ')
        else:
            lineL = string.split(line, sep=options.tab_word)
        i += 1
        for j in range(len(lineL)):
            if len(lineL[j]) >= 40:
                lineL[j] = lineL[j][:18] + '.'*4 + lineL[j][-18:]
        lines.append(lineL)
    in_f.close()
    header = []
    for i in range(len(lines[0])):
        header.append("col*"+str(i))
    lines.insert(0, header)
    if options.direction == 'v':
        lines = transpose(lines)
    
    terminal_w = get_terminal_width_resize()
    len_m = [map(len, x) for x in lines]
    max_cell = map(max, transpose(len_m))
    
    print_matrix(max_cell, lines, terminal_w)

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
#-------------------------------------------------------------------------------
# EOF

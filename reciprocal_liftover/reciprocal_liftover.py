#! /usr/bin/env python

import os
import sys
import yaml
import glob
import subprocess
import string
import time

config_name = sys.argv[1]
config_f = open(config_name, 'r')
config = yaml.load(config_f)
config_f.close()

print(config)

class genomicInterval:
    """class for bed interval"""
    def __init__(self, chrom, start, end, strand):
        self.chrom = chrom
        self.start = int(start)
        self.end = int(end)
        self.strand = strand

def formatGoBed(inputBed):
    queryIDs = []
    lines = [string.strip(x) for x in open(inputBed, 'r')]
    out_f = open("tmp_in.bed", 'w')
    for line in lines:
        if line.startswith('#'):
            continue;
        lineL = string.split(line, sep='\t')
        tmpID = '#'.join(lineL)
        lineL[3] = tmpID
        queryIDs.append(tmpID)
        out_f.write('\t'.join(lineL)+'\n')
    out_f.close()
    return queryIDs

def formatBackBed(inputBed):
    lines = [string.strip(x) for x in open(inputBed, 'r')]
    out_f = open("tmp_back.bed", 'w')
    for line in lines:
        if line.startswith('#'):
            continue;
        lineL = string.split(line, sep='\t')
        newID = lineL[3]
        del lineL[3]
        tmpID = '#'.join(lineL)
        lineL.insert(3, tmpID + "#" + newID)
        out_f.write('\t'.join(lineL)+'\n')
    out_f.close()

def doLiftOver(config, chain, inputBed, outputBed, unmappedBed):
    cmds = ["liftOver"]
    cmds.append("-minMatch=" + str(config["minMatch"]))
    cmds.append("-multiple")
    cmds.append("-minBlocks=" + str(config["minBlocks"]))
    cmds.append(inputBed)
    cmds.append(chain)
    cmds.append(outputBed)
    cmds.append(unmappedBed)
    p = subprocess.Popen(cmds, stdout=subprocess.PIPE)
    print p.communicate()

def judgeOverlap(inA, inB):
    if inA.chrom != inB.chrom:
        return None
    if inA.strand != inB.strand:
        return None
    lenA = abs(inA.end - inA.start)
    lenB = abs(inB.end - inB.start)
    lenGenomic = abs(max(inA.end, inB.end) - min(inA.start, inB.start))
    if (lenA + lenB) <= lenGenomic:
        return None
    else:
        return abs((lenA + lenB) - lenGenomic)

def isOverlapped(lineL, oriL):
    '''
    Parse the result line to judge if it is the right hit.
    If not hit, return None.
    If hit, return the overlap nts.
    '''
    reciHit = genomicInterval(lineL[0], lineL[1], lineL[2], lineL[5])
    oriEntry = genomicInterval(oriL[5], oriL[6], oriL[7], oriL[10])
    return judgeOverlap(reciHit, oriEntry)

def parseReci(reci_bed_name, queryIDs, inputBed):
    '''
    Parse the results of the reciprocal liftover.
    If multiple entries exist, then only keep the longest overlapped.
    Write to the file and return the unmapped entries.
    '''
    hitIDsDict = {}
    lines = [string.strip(x) for x in open(reci_bed_name, 'r')]
    for line in lines:
        lineL = string.split(line, sep='\t')
        oriL = lineL[3].split('#')
        tmpID = '#'.join(oriL[5:])

        overlappedNT = isOverlapped(lineL, oriL)
        if overlappedNT is not None:
            if tmpID not in hitIDsDict:
                hitIDsDict[tmpID] = [None, [], []]
            if (hitIDsDict[tmpID][0] is None) or (hitIDsDict[tmpID][0] < overlappedNT):
                hitIDsDict[tmpID] = [overlappedNT, lineL, oriL]
            if tmpID in queryIDs:
                queryIDs.remove(tmpID)

    out_f = file(inputBed.replace(".bed", "_reci.bed"), 'w')
    for key, value in hitIDsDict.items():
        lineL = value[1]
        oriL = value[2]
        newLine = oriL[5:] + oriL[:4] + [oriL[8], str(value[0]), oriL[4]]
        out_f.write('\t'.join(newLine)+'\n')
    return queryIDs

for inputBed in config['input_beds']:

    ## convert to target genome
    print(inputBed)
    queryIDs = formatGoBed(inputBed)
    doLiftOver(config, config["go_chain"], "tmp_in.bed",
                "tmp_go.bed", "tmp_go_unmapped.bed")

    ## convert back to original genome
    formatBackBed("tmp_go.bed")
    doLiftOver(config, config["back_chain"], "tmp_back.bed",
                "tmp_reci.bed", "tmp_reci_unmapped.bed")

    unmapped_entries = parseReci("tmp_reci.bed", queryIDs, inputBed)
    print("%d entries are not mapped to new genome." % len(unmapped_entries))

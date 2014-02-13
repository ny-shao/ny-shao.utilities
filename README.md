# README

A repo for my utilities.

* table_header.py

Just for the boring counting before I do R scripting. Check the columns of the tables.

Options:
```
  -h, --help            show this help message and exit
  -l LINE_NO, --lines=LINE_NO
                        header lines to be printed.
  -d DIRECTION, --direction=DIRECTION
                        direction of printing. v or h.
  -t TAB_WORD, --tab=TAB_WORD
                        tab word. s or t. s: space. t: tab.
```

For example:
```bash
./table_head.py annotatePeaks.txt # It is a table generated by HOMER of a ChIP-seq dataset.

col*0                                   |col*1|col*2|col*3|col*4 
PeakID (cmd=/home/....t/TvsC_down_HOMER)|Chr  |Start|End  |Strand
------------------------------------------------------------------------
col*5     |col*6                  |col*7     |col*8              
Peak Score|Focus Ratio/Region Size|Annotation|Detailed Annotation
------------------------------------------------------------------------
col*9          |col*10            |col*11   |col*12         
Distance to TSS|Nearest PromoterID|Entrez ID|Nearest Unigene
------------------------------------------------------------------------
col*13        |col*14         |col*15   |col*16    |col*17          
Nearest Refseq|Nearest Ensembl|Gene Name|Gene Alias|Gene Description
------------------------------------------------------------------------
col*18   
Gene Type
```

* intersectSet.py:

A script mimic of [bedtools](https://github.com/arq5x/bedtools‎) for gene lists.

```bash
> ./intersectSet.py --help
usage: intersectSet.py [-h] -a A -b B [-v]

Mimic of bedtools to manipulate gene list set

optional arguments:
  -h, --help  show this help message and exit
  -a A        SetA
  -b B        SetB
  -v          specific of setA
```

* convertEnsembl2Symbol.R

A script to add a column of gene symbol to correspondent ensembl id.

```
 args[1]: file name, only csv or txt
 args[2]: column number of ensembl_id
 args[3]: if "1", input file with header; other: no header.
```
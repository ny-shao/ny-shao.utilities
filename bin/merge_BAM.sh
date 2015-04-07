#! /usr/bin/env bash

OUTPUT_BAM=${1}
SAMTOOLS_BUFF=${2}
CORES=${3}
IN_BAMS=$4

function mergeBAMS(){
    #  declare -a IN_BAMS=("${!2}")
    IN_BAMS=( ${2} )
    OUT_BAM=$1
    samtools merge ${OUT_BAM} ${IN_BAMS[@]}
}
export -f mergeBAMS

mergeBAMS ${OUTPUT_BAM/.bam/_unsorted.bam} "${IN_BAMS}"
samtools sort -@ ${CORES} -m ${SAMTOOLS_BUFF} ${OUTPUT_BAM/.bam/_unsorted.bam} ${OUTPUT_BAM/.bam/}
samtools index ${OUTPUT_BAM}
rm ${OUTPUT_BAM/.bam/_unsorted.bam}

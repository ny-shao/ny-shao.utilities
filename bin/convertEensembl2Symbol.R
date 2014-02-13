#! /usr/bin/env Rscript

## Convert ensembl id in the table to gene symbol in mm9.
## args[1]: file name, only csv or txt
## args[2]: column number of ensembl_id
## args[3]: if "1", input file with header; other: no header.

args <- commandArgs(T)

ensembl.col <- as.numeric(args[2])

if (args[3] == "1"){
	header = TRUE
}else{
	header = FALSE
}

## read file by suffix of file
require(tools)
file.type <- file_ext(args[1])
if (file.type == "txt"){
	file.name <- sub('.txt$', '', basename(args[1]))
	input.table <- read.table(args[1], header=header, sep="\t", comment.char="",
		quote="", stringsAsFactors=FALSE)
}else if(file.type == "csv"){
	file.name <- sub('.csv$', '', basename(args[1]))
	input.table <- read.csv(args[1], header=header, comment.char="",
		stringsAsFactors=FALSE)
}else{
	stop("Only csv and txt are supported now.")
}


require(biomaRt)
mart <- useMart(biomart="ensembl", dataset="mmusculus_gene_ensembl")
results <- getBM(attributes = c("ensembl_gene_id", "mgi_symbol"), 
	filters = "ensembl_gene_id", values = input.table[,ensembl.col], mart = mart)
colnames(input.table)[ensembl.col] <- "ensembl_gene_id"
input.table <- merge(input.table, results, by="ensembl_gene_id",
	all.x=TRUE)

write.csv(input.table, file=paste(file.name, "_symbol.csv", sep=""))
library(VirFinder)

files <- list.files(path="/contigs", pattern="*.fasta", full.names=TRUE, recursive=FALSE)

lapply(files, function(x) {
    predResult <- VF.pred(x)
    #predResult$qvalue <- VF.qvalue(predResult$pvalue)
    predResult$qvalue <- p.adjust(predResult$pvalue, method="BH")
    t <- predResult[order(predResult$pvalue),]
    prefix <- sub(".*\\/(\\d+)_.*", "\\1", x)
    write.csv(t, '/output/virfinder_out')
})


#files <- list.files(path="path/to/dir", pattern="*.txt", full.names=TRUE, recursive=FALSE)
#lapply(files, function(x) {
#    t <- read.table(x, header=TRUE) # load file
#    # apply function
#    out <- function(t)
#    # write to file
#    write.table(out, "path/to/output", sep="\t", quote=FALSE, row.names=FALSE, col.names=TRUE)
#})

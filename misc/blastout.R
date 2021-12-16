library(ggplot2)
library(hash)

blastn_out <- read.csv("/Users/tobias/spacer_search_results_blastn_100000.out", sep="\t", header=F)
blastn_out

dim(blastn_out)
class(blastn_out)

evalues <- blastn_out[,11]
header <- blastn_out[,1]
matches <- blastn_out[,2]

length(header)
length(unique(header))
unique(header)

summary(evalues)
boxplot(evalues)

acc_list <- c()
spacer_pos <- c()
refseq <- c()
for (row in 1:nrow(blastn_out)){
  header <- as.character(blastn_out[row,1])
  split_header <- strsplit(header,"|",fixed=T)
  for (i in split_header[[1]]){
    acc <- as.character(i)
    split <- strsplit(acc,"_",fixed=T)
    ref <- paste(split[[1]][1],split[[1]][2],sep='_')
    pos <- split[[1]][4]
    crispr_nr <- split[[1]][3]
    spacer_pos <- append(spacer_pos,pos)
    refseq <- append(refseq,ref)
    acc_list <- append(acc_list,acc)
    # if(is.null(acc_list$acc)){
    #   acc_list[[acc]] <- 1
    # }
    # else{
    #   print("else")
    #   acc_list$acc <- acc_list$acc + 1
    # }
  }
}


summary(keys(acc_list))








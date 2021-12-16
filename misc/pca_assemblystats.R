library(ggplot2)
library("FactoMineR")
library("factoextra")
library("corrplot")

data_1 <- assembly_stats_V1
data_5 <- assembly_stats_V5
data_6 <- assembly_stats_V6
data_10 <- assembly_stats_V10
data_br <- assembly_stats_vDNA

data_1 <- assembly_stats_MG1
data_5 <- assembly_stats_MG5
data_6 <- assembly_stats_MG6
data_10 <- assembly_stats_MG10
head(data_1)

####################################################
#boxplots
columns <- c(20,1,8,4,19)
labels <- c('percent_mapped','number_of_contigs','max_contig','contig_N50','contig_avg_coverage')

j <- 1
for (i in columns){
  #get columns
  V1 <- data_1[,i]
  V5 <- data_5[,i]
  V6 <- data_6[,i]
  V10 <- data_10[,i]
  VBR <- data_br[,i]
  
  df <- data.frame(V1,V5,V6,V10,VBR)
  stacked <- stack(df)
  stacked
  names(stacked)[1] <- labels[j]
  names(stacked)[2] <- "sample"
  j = j+1
  
  plot = ggplot(data = stacked, aes(y=stacked[,1], x=sample)) + geom_boxplot() +theme(text = element_text(size=20, face="bold"))
  plot = plot + ylab(labels[j])
  print(plot)
}

####################################################
#PCA
data <- data_V5
#data <- data[,-10] #remove filename column
#data.active <- data[,-(10:12),drop=FALSE]
head(data)
quanti.sup <- data[,14:18, drop = FALSE]
head(quanti.sup)
data <- data[,-3] #drop gap_pct

res.pca <- PCA(data[,-(9:17),drop=FALSE], graph = FALSE,scale=TRUE) #exlude column assembler, filename, job_nr, ale, ks
data
v1 <- data$ale_score
v2 <- (v1-min(v1))/(max(v1)-min(v1))
v2

fviz_pca_ind(res.pca,
             col.ind = "cos2", # Color by the quality of representation
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE     # Avoid text overlapping
)
fviz_pca_var(res.pca,
             col.var = "contrib", # Color by contributions to the PC
             gradient.cols = c("#00AFBB", "#E7B800", "#FC4E07"),
             repel = TRUE     # Avoid text overlapping
)
fviz_pca_biplot(res.pca, repel = TRUE,
                col.var = "#2E9FDF", # Variables color
                col.ind = "#696969"  # Individuals color
)
head(res.pca$var$cos2)
corrplot(res.pca$var$contrib, is.corr=FALSE)
# 
# groups <- as.factor(data$assembler)
# fviz_pca_ind(res.pca,
#              col.ind = groups, # color by groups
#              palette = c("#00AFBB",  "#FC4E07"),
#              addEllipses = FALSE, # Concentration ellipses
#              ellipse.type = "confidence",
#              legend.title = "Groups",
#              repel = TRUE
# )

# Predict coordinates and compute cos2
quanti.coord <- cor(quanti.sup, res.pca$x)
quanti.cos2 <- quanti.coord^2
# Graph of variables including supplementary variables
p <- fviz_pca_var(res.pca,repel=TRUE)
fviz_add(p, quanti.coord, color ="blue", geom="arrow")


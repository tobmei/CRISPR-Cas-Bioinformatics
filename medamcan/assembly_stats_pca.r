library("FactoMineR")
library("factoextra")
library("plotrix")
library("qvalue")
library("overlap")
library("dplyr")
library("reshape2")
library("VennDiagram")
library("corrplot")
library("stringr")


#assembly stats
data <- nancy_viral_ref_assembly_stats
var(data$place)
var(data$insert)
var(data$kmer)
var(data$depth)

#data <- nancy_viral_predictions
data <- bioreaktor_viral_predictions 
data$set <- factor(data$set, levels=c("MVS","0","1","2","3","4","5","6","7","8","9","10",
                                         "11","12","13","14","15","16","17","18","19","20",
                                         "21","22","23","24","25","26","27","28","29","30",
                                         "31","32","33","34","35","36","37","38","39","40",
                                         "41","42","43","44","45","46","47","48","49","50",
                                         "51","52","53","54","55","56","57","58","59"))
#data$prune <- as.factor(data$prune)
#data$bubble <- as.factor(data$bubble)
#data$cl <- as.factor(data$cl)
data <- data[!data$set == "MVS",]
data 
data.active <- data[,2:14]
head(data.active)
res.pca <- PCA(data.active, graph = FALSE)
print(res.pca)
eigenvalues <- res.pca$eig
head(eigenvalues[, 1:2])
fviz_screeplot(res.pca, ncp=10)
fviz_pca_var(res.pca)
fviz_pca_ind(res.pca, col.ind="cos2",repel=TRUE) +
  scale_color_gradient2(low="blue", mid="white",high="red", midpoint=0.50)
fviz_pca_biplot(res.pca,  geom = "text", repel=TRUE)
res.pca <- PCA(data,quanti.sup=15:17, graph=FALSE)
fviz_pca_var(res.pca)

##distribution of predictions -> dvf more effected by pruning parameters -> higher variance
sqrt(var(data$dvf_total))
sqrt(var(data$vf_virus))
dat.m <- melt(data,id.vars='set', measure.vars=c('dvf_total','vf_virus'))
ggplot(dat.m) + geom_boxplot(aes(x=variable, y=value))

##correlations between viral predictions and parameters
colnames(data)[2] <- "dvf"
colnames(data)[4] <- "unique_genes"
colnames(data)[19] <- "total_length"
head(data)
cordat <- select(data,dvf,vf_virus,vf_vb,vf_short,vf_pc,vf_p,vf_c,prune,bubble,cl,total_viruses,unique_genes)
cordat
cor.mat <- round(cor(cordat),2)
corrplot(cor.mat, type="upper", order="hclust", tl.col="black", tl.srt=45, addCoef.col = "black")
ggplot(data, aes(x=set)) + 
  geom_point(aes(y=dvf_total)) +
  geom_point(aes(y=vf_virus)) +
  geom_point(aes(y=vf_vb)) +
  geom_point(aes(y=vf_short)) +
  geom_point(aes(y=vf_pc)) +
  geom_point(aes(y=vf_c)) +
  geom_point(aes(y=vf_p)) +
  geom_point(aes(y=total_viruses)) 
  #geom_point(aes(y=contig_bp))


#coverage of viral contigs
#dat1 <- nancy_1
#dat2 <- nancy_05
#dat3 <- nancy_025
dat1 <- bio_1
dat2 <- bio_05
dat3 <- bio_025
dat <- data.frame(dat1$V2,dat2$V2,dat3$V2)
names(dat) <- c("high", "mid", "low")
mean(dat$high)
median(dat$high)
sqrt(var(dat$high))
mean(dat$mid)
median(dat$mid)
sqrt(var(dat$mid))
mean(dat$low)
median(dat$low)
sqrt(var(dat$low))
dat <- melt(dat)
ggplot(dat, aes(x=variable,y=value)) + geom_boxplot() + scale_y_log10()



##create plots for deepvirfinder output

#dvf_data <- bioreaktor_dvf_combined_1kb
#dvf_data <- nancy_dvf_combined_1kb
dvf_data1 <- opt_dvf_combined
dvf_data2 <- gen_dvf_combined
median(dvf_data1$V4)
median(dvf_data2$V4)
head(dvf_data)
dvf_data
df <- data.frame()
df_count <- data.frame()

ggplot(dvf_data, aes(y=dvf_data$V3, group=dvf_data$V1)) + geom_boxplot() + scale_y_log10() +labs(y="") +theme(axis.title.x=element_blank(),
                                                                                                              axis.text.x=element_blank(),
                                                                                                              axis.ticks.x=element_blank())

l <- cbind(dvf_data1$V3,dvf_data2$V3)
s <-cbind(dvf_data1$V4,dvf_data2$V4)

colnames(l) <- c("opt_length", "def_length")
colnames(s) <- c("opt_score", "def_score")
datl <- melt(l)
dats <- melt(s)
ggplot(datl, aes(y=datl$value, group=datl$Var2, fill=datl$Var2)) + geom_boxplot() + scale_y_log10() +theme(axis.title.x=element_blank(),
                                                                                                           axis.text.x=element_blank(),
                                                                                                           axis.ticks.x=element_blank(),
                                                                                                           legend.position = "none") +ylab("length")
ggplot(dats, aes(y=dats$value, group=dats$Var2, fill=dats$Var2)) + geom_boxplot() + scale_y_log10() +theme(axis.title.x=element_blank(),
                                                                                                           axis.text.x=element_blank(),
                                                                                                           axis.ticks.x=element_blank(),
                                                                                                           legend.position = "none") +ylab("score")

for (i in 0:59){
tmp <- dvf_data[dvf_data[,1]==i,]
# estimate q-values (false discovery rates) based on p-values
#tmp$qvalue <- qvalue(tmp$V4, lambda=0)$qvalues
tmp <-tmp[tmp[,5]<0.05,]
tmp <-tmp[tmp[,4]>=0.95,]
nr <- nrow(tmp) #number of significant viral contigs
nr12kb <- nrow(tmp[tmp[,3]<=2000,])
nr23kb <- nrow(tmp[tmp[,3]>2000 & tmp[,3]<=3000,])
nr34kb <- nrow(tmp[tmp[,3]>3000 & tmp[,3]<=4000,])
nr45kb <- nrow(tmp[tmp[,3]>4000 & tmp[,3]<=5000,])
nr510kb <- nrow(tmp[tmp[,3]>5000 & tmp[,3]<=10000,])
nr1020kb <- nrow(tmp[tmp[,3]>10000 & tmp[,3]<=20000,])
nr2050kb <- nrow(tmp[tmp[,3]>20000 & tmp[,3]<=50000,])
nr50kb <- nrow(tmp[tmp[,3]>50000,])
#nr100kb <- nrow(tmp[tmp[,3]>=100000,])
tmp <- tmp[order(tmp$V4),]
df <- rbind(df,tmp)
df_count <- rbind(df_count,c(i,nr,nr12kb,nr34kb,nr45kb,nr510kb,nr1020kb,nr2050kb,nr50kb))
}
df
df_count
#df <- df[order(df$nr, decreasing=TRUE),]
#df$nr <- as.factor(df$nr)
df$V1 <- as.factor(df$V1)
#df <- df[order(df$V2, decreasing=TRUE),]
ggplot(df, aes(x=V1)) + geom_bar() +
  theme(axis.text.x = element_text(angle = 60)) +
  xlab("Assembly set") + 
  ylab("Number of contigs")


dvf_metaviral <- nancy_metaviral_1kb.fasta_gt1bp_dvfpred
dvf_metaviral <- dvf_metaviral[dvf_metaviral[,3] >= 0.95,]
dvf_metaviral <- dvf_metaviral[dvf_metaviral[,4] < 0.05,]
(dvf_metaviral)
nr12kb <- nrow(dvf_metaviral[dvf_metaviral[,2]<=2000,])
nr23kb <- nrow(dvf_metaviral[dvf_metaviral[,2]>2000 & dvf_metaviral[,2]<=3000,])
nr34kb <- nrow(dvf_metaviral[dvf_metaviral[,2]>3000 & dvf_metaviral[,2]<=4000,])
nr45kb <- nrow(dvf_metaviral[dvf_metaviral[,2]>4000 & dvf_metaviral[,2]<=5000,])
nr510kb <- nrow(dvf_metaviral[dvf_metaviral[,2]>5000 & dvf_metaviral[,2]<=10000,])
nr1020kb <- nrow(dvf_metaviral[dvf_metaviral[,2]>10000 & dvf_metaviral[,2]<=20000,])
nr2050kb <- nrow(dvf_metaviral[dvf_metaviral[,2]>20000 & dvf_metaviral[,2]<=50000,])
nr50kb <- nrow(dvf_metaviral[dvf_metaviral[,2]>50000,])
c(nr12kb,nr23kb,nr34kb,nr45kb,nr510kb,nr1020kb,nr2050kb,nr50kb)
ggplot(dvf_metaviral) + geom_jitter(aes(x=score,y=len))

df_count <- rbind(df_count,c("MV",nr12kb,nr23kb,nr34kb,nr45kb,nr510kb,nr1020kb,nr2050kb,nr50kb))
df_count[,1] <- as.factor(df_count[,1])
df_count
df_long

names(df_count) <- c("set","1-2kb","2-3kb","3-4kb","4-5kb","5-10kb","10-20kb","20-50kb",">50kb")
df_long <- melt(df_count,id="set")
df_long$value <- as.numeric(df_long$value)
colnames(df_long)[2] <- "Size"
df_long$set <- factor(df_long$set, levels=c("0","1","2","3","4","5","6","7","8","9","10",
                                            "11","12","13","14","15","16","17","18","19","20",
                                            "21","22","23","24","25","26","27","28","29","30",
                                            "31","32","33","34","35","36","37","38","39","40",
                                            "41","42","43","44","45","46","47","48","49","50",
                                            "51","52","53","54","55","56","57","58","59"))
ggplot(df_long, aes(x=set, y=value)) + geom_point(aes(color=Size )) + scale_y_log10() + 
  theme(axis.text.x = element_text(angle = 60)) +
  xlab("Assembly set") + 
  ylab("Number of contigs")

ggplot(df[df[,3]>=5000,], aes(x=V1, y=V3)) + geom_boxplot(aes(group=V1))
ggplot(df[df[,3]>=10000,], aes(x=V1, y=V3)) + geom_boxplot(aes(group=V1))
ggplot(df[df[,3]>=50000,], aes(x=V1, y=V3)) + geom_boxplot(aes(group=V1)) + geom_jitter(aes(y=V4))

#ggplot(df, aes(x=reorder(V1,nr,FUN=median), y=V2)) + geom_boxplot(aes(group=V2))
ggplot(df, aes(x=V1)) + geom_boxplot(aes(y=V4))


##dvf vs viralverify
#dvf_comb <- nancy_dvf_combined_1kb
#vf_comb <- nancy_viralverify_combined
dvf_comb <- opt_dvf_combined
vf_comb <- opt_vf_combined
#dvf_comb <- bioreaktor_dvf_combined_1kb
#vf_comb <- bioreaktor_viralverify_combined
intersection_df <- data.frame()
score_list <- c()
#for each assembly set, get intersections dvf vs vf
for (i in 0:59){
dvf <- dvf_comb[dvf_comb[,1]==i,]
vf <- vf_comb[vf_comb[,1]==i,]
vf$V6 <- as.numeric(vf$V6)
#score_list <- c(score_list, c(i))

dvf_virus <- dvf[dvf[,4]>=0.50 & dvf[,5]<0.05,]$V2 
vf_virus <- vf[vf[,3]=="Virus",]$V2
vf_vb <- vf[vf[,3]=="Uncertain - viral or bacterial",]$V2
vf_short <- vf[vf[,3]=="Uncertain - too short",]$V2
vf_pc <- vf[vf[,3]=="Uncertain - plasmid or chromosomal",]$V2
vf_c <- vf[vf[,3]=="Chromosome",]$V2
vf_p <- vf[vf[,3]=="Plasmid",]$V2
vf_virus_gene_names <- vf[vf[,3]=="Virus",]$V7
#score_list[i] <-c(score_list,vf[vf[,3]=="Virus",]$V6)
#print(mean(vf[vf[,3]=="Virus",]$V6))
#print(median(vf[vf[,3]=="Virus",]$V6))
#print(max(vf[vf[,3]=="Virus",]$V6))
#print(sqrt(var(vf[vf[,3]=="Virus",]$V6)))

l1 <- intersect(dvf_virus,vf_virus)
l2 <- intersect(dvf_virus,vf_short)
l3 <- intersect(dvf_virus,vf_pc)
l4 <- intersect(dvf_virus,vf_c)
l5 <- intersect(dvf_virus,vf_p)
total_viruses <- (length(dvf_virus) + length(vf_virus)) - length(l1) - length(l3) - length(l4) - length(l5)

##get contig ids for total viruses
u <- (union(dvf_virus,vf_virus))
i1 <- setdiff(u,vf_pc)
i2 <- setdiff(i1,vf_c)
i3 <- setdiff(i2,vf_p)
#write.table(i3, paste("/home/tob/toStick/virus_assembly/bioreaktor/viral_contig_ids/",i,sep=""), quote=FALSE,col.names = F, row.names = F) 

intersection_df <- rbind(intersection_df, c(i,length(dvf_virus),length(vf_virus),length(vf_vb),length(vf_short),
                                            length(vf_pc),length(vf_c),length(vf_p),length(l1),length(l2),length(l3),length(l4),length(l5),total_viruses))
}

names(intersection_df) <- c("set", "dvf_total", "vf_virus", "vf_vb", "vf_short", "vf_pc", "vf_c", "vf_p",
                            "dvf-vf.v", "dvf-vf.short", "dvf-vf.pc", "dvf-vf.c", "dvf-vf.p", "total_viruses")

## add metaviralspades results
dvf_metaviral <- nancy_metaviral_1kb.fasta_gt1bp_dvfpred
vf_metaviral <- nancy_metaviral_1kb_result_table
#vf_metaviral <- bioreaktor_metaviral_1kb_result_table
#dvf_metaviral <- bioreaktor_metaviral_1kb.fasta_gt1bp_dvfpred
dvf_metaviral_virus <- dvf_metaviral[dvf_metaviral[,3]>=0.95 & dvf_metaviral[,4]<0.05,]$name
vf_virus <- vf_metaviral[vf_metaviral[,2]=="Virus",]$V1
vf_vb <- vf_metaviral[vf_metaviral[,2]=="Uncertain - viral or bacterial",]$V1
vf_short <- vf_metaviral[vf_metaviral[,2]=="Uncertain - too short",]$V1
vf_pc <- vf_metaviral[vf_metaviral[,2]=="Uncertain - plasmid or chromosomal",]$V1
vf_c <- vf_metaviral[vf_metaviral[,2]=="Chromosome",]$V1
vf_p <- vf_metaviral[vf_metaviral[,2]=="Plasmid",]$V1
l1 <- length(intersect(dvf_metaviral_virus,vf_virus))
l2 <- length(intersect(dvf_metaviral_virus,vf_short))
l3 <- length(intersect(dvf_metaviral_virus,vf_pc))
l4 <- length(intersect(dvf_metaviral_virus,vf_c))
l5 <- length(intersect(dvf_metaviral_virus,vf_p))
total_viruses <- (length(dvf_metaviral_virus) + length(vf_virus)) - l1 - l3 - l4 - l5

#intersection_df$set <- as.factor(intersection_df$set)
intersection_df <- rbind(intersection_df, c(as.factor("MVS"),length(dvf_metaviral_virus),length(vf_virus),length(vf_vb),length(vf_short),
                                            length(vf_pc),length(vf_c),length(vf_p),l1,l2,l3,l4,l5,total_viruses))


intersection_df
ggplot(intersection_df, aes(x=set)) + geom_point(aes(reorder(set,-total_viruses), total_viruses))
write.table(intersection_df, "/home/tob/toStick/virus_assembly/bioreaktor/bioreaktor_viral_predictions.txt", sep=",") 

##get contig ids for total viruses
u <- (union(dvf_metaviral_virus,vf_virus))
i1 <- setdiff(u,vf_pc)
i2 <- setdiff(i1,vf_c)
i3 <- setdiff(i2,vf_p)
length(i3)
write.table(i3,"/home/tob/toStick/virus_assembly/bioreaktor/viral_contig_ids/mvs", quote=FALSE,col.names = F, row.names = F) 

venn.diagram(x=list(dvf_virus, vf_virus, vf_vb, vf_short, vf_pc),
             category.names=c("dvf", "vf", "vf-viral or bacterial", "vf-too short", "vf-pc"),
             output=TRUE,filename="file")



# dvr contigs length vs score
dat <- df[df[,1]==0,]
ggplot(df, aes(x=V2, y=V3)) + geom_point()
ggplot(df, (aes(x=V1, y=V4))) + geom_boxplot() + geom_jitter(width=0.15,aes(color=V3))



##
##create cluster plots for genomic distances of contig sets

#mash_dist <- bioreaktor_contigs_dist_1kb
#mash_dist <- bioreaktor_contigs_dist_5kb
#mash_dist <- nancy_contigs_dist_1kb
mash_dist <- nancy_contigs_dist
#mash_dist <- bioreaktor_contigs_dist
#mash_dist <- nancy_contigs_dist_5kb

d <- dist(mash_dist) 
mash_dist

#plot(hclust(as.dist(mash_dist), method="average"))
#mash_dist <- as.dist(mash_dist)

res <- hcut(mash_dist, k = 2, stand = TRUE, hc_method="ward.D2")
fviz_dend(res, rect = TRUE)
fviz_silhouette(res, label=TRUE)
fviz_cluster(res)

##create silhouette plot to determine number of clusters
widths <- c()
cluster <- c()
for (i in 2:14){
  res <- hcut(mash_dist, k = i, stand = TRUE, hc_method="ward.D2")
  cluster <- rbind(cluster,i)
  widths <- rbind(widths,res$silinfo$avg.width)
}
sil_widths <- data.frame(cluster,widths)
sil_widths
ggplot(sil_widths, aes(x = cluster, y = widths)) + 
  geom_point() + geom_line() 


##plot kmer statistics
data <- kat
data <- kat_viral
ggplot(data, aes(x=V1, y=V2)) + geom_point() + scale_y_log10() + scale_x_log10()
ggplot(data, aes(x=V2)) + geom_density()


##plot viralverify output
#data <- nancy_viralverify_combined
#data <- bioreaktor_viralverify_combined
data <- gen_vf_combined
#data <- opt_vf_combined
data$V1 <- as.factor(data$V1)
#data$V6 <- as.numeric(data$V6)

#index1 <- with(data, grepl("Virus", V3))
#data <- data[index1,]
colnames(data)[3] <- "Classification"

data <- data[complete.cases(data), ]
data <- data[data[,3]!="Uncertain - too short", ]
ggplot(data, aes(x=V1, fill=Classification)) +
  geom_bar( color="#e9ecef", position="stack") + theme(axis.text.x = element_text(angle = 90)) +
  ylab("Number of contigs") + theme(axis.title.x=element_blank(),
                                     axis.text.x=element_blank(),
                                     axis.ticks.x=element_blank()) + scale_y_log10()
#ggplot(data, (aes(y=V4))) + geom_jitter(aes(x=V1, color=V6)) + scale_color_gradient(low="blue", high="red")
#ggplot(data, (aes(y=V6))) + geom_boxplot(aes(x=V1))
ggplot(data, aes(x=V1, fill=V3)) +
  geom_line(stat="count") +
  

data


data <- data[data[,3]=="Virus",]
df <- data.frame()
##count the number of viruses for each set
for (i in 0:59){
  tmp <- data[data[,1]==i,]
  nr_viruses <- nrow(tmp) #number of viruses
  df <- rbind(df,c(i,nr_viruses))
}
df
ggplot(df, (aes(x=df[,1],y=df[,2]))) + geom_line()


#mix assembly analysis
data <- nancy_viral_mid[,2:12]
#data <- nancy_viral_low[,2:12]

data
res.pca <- PCA(data,quanti.sup=1:3, graph=FALSE)
fviz_pca_var(res.pca)

fit <- lm(duplicates ~ prune * bubble * cl, data=data)
summary(fit) 
fit <- lm(containments ~ prune * bubble * cl, data=data)
summary(fit) 
fit <- lm(contig_bp ~ prune * bubble * cl, data=data)
summary(fit) 
fit <- lm(overlaps ~ prune * bubble * cl, data=data)
summary(fit) 
anova(fit) 


#blast results
data <- blast_nacbi_ref_result_combined
head(data)
data <- reshape(data, idvar = "acc", timevar = "database", direction = "wide")
head(data)
data <- data[!(data$matches.nt==0),]
data

ggplot(data) + geom_boxplot(aes(y=matches.viruses)) 


###CRISPR
common_ids <- common_ids
#data <- opt_assembly_crispr_dist
data <- cas_type_distribution
#data <- gen_assembly_crispr_dist
data_cp <- data
for(i in 1:nrow(data_cp)) {
  if (!is.element(data_cp[i,1], common_ids)){
    data <- data[-i,]
  }
}
nrow(data)
data <- melt(data,id.vars='set')
colnames(data) <- c("sample","Subtype", "count")

#add type coloumn
data$Type <- c("A")
data$Subtype <- as.character(data$Subtype)
for(i in 1:nrow(data)) {
  row <- data[i,]
  type <- str_match(row[2],"(CAS\\..*)\\..*")[,2]
  data[i,4] <- type
}
data$Type <- as.factor(data$Type)
data$Subtype <- as.factor(data$Subtype)

#data <- data[data$Type=="CAS.VI",]
bp <- ggplot(data, aes(x="", y=count, fill=Subtype)) +  geom_bar(width = 1, stat = "identity")
pie <- bp + coord_polar("y", start=0)
#pie
# blank_theme <- theme_minimal()+
#   theme(
#     axis.title.x = element_blank(),
#     axis.title.y = element_blank(),
#     panel.border = element_blank(),
#     panel.grid=element_blank(),
#     axis.ticks = element_blank(),
#     plot.title=element_text(size=14, face="bold")
#   )
# pie + blank_theme
pie + theme_void()

#total system
sum(data$count)
#per type
ggplot(data, aes(x=Type, y=count, fill=Type)) +  geom_bar(width = 1, stat = "identity")

#coverage
gen <- gen_dvf_coverage
opt <- opt_dvf_coverage
dat <- cbind(gen,opt)

ggplot(opt, aes(y=opt$V1)) + geom_boxplot() + scale_y_log10() +theme(axis.title.x=element_blank(),
                                                                     axis.text.x=element_blank(),
                                                                     axis.ticks.x=element_blank()) + ylab(("coverage"))

ggplot(gen, aes(y=gen$V1)) + geom_boxplot() + scale_y_log10() +theme(axis.title.x=element_blank(),
                                                                     axis.text.x=element_blank(),
                                                                     axis.ticks.x=element_blank()) + ylab("coverage")
median(gen$V1)
mean(gen$V1)
sqrt(var(gen$V1))
median(opt$V1)
mean(opt$V1)
sqrt(var(opt$V1))


data <- protospacer_discovery
colnames(data) <- c("a", "b", "c", "d", "default", "optimized", "g")
data <- melt(data, id.vars="a", measure.vars=c("default","optimized"))
colnames(data) <- c("a","assembly","percentage")
ggplot(data, aes(y=percentage, color=assembly)) + geom_boxplot()




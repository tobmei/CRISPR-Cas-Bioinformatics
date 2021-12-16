library(SRAdb)
library(ggplot2)

getSRAdbFile()

sqlfile <- file.path("/Users/tobias/SRAmetadb.sqlite")

sra_con <- dbConnect(SQLite(),sqlfile)
sra_tables <- dbListTables(sra_con)

sra_tables

dbListFields(sra_con,"experiment")
dbListFields(sra_con,"metainfo")
dbListFields(sra_con,"sra")
dbListFields(sra_con,"sra_ft")
dbListFields(sra_con,"sra_ft_content")
dbListFields(sra_con,"sra_ft_segdir")
dbListFields(sra_con,"sra_ft_segments")
dbListFields(sra_con,"sample")
dbListFields(sra_con,"run")
dbListFields(sra_con,"study")
dbListFields(sra_con,"submission")
dbListFields(sra_con,"description")



query <- "select library_strategy from sra"
lib_strat <- dbGetQuery(sra_con,query)
unique.data.frame(lib_strat)
table(unlist(lib_strat))

query <- "select platform from sra"
lib_strat <- dbGetQuery(sra_con,query)
unique.data.frame(lib_strat)
table(unlist(lib_strat))

query <- "select library_source from sra"
lib_src <- dbGetQuery(sra_con,query)
unique.data.frame(lib_src)

query <- "select run_accession, sample_accession, platform from sra where (library_source = 'METAGENOMIC' AND library_strategy ='WGS')"
metag_wgs_runacc <- dbGetQuery(sra_con,query)
dim(metag_wgs_runacc)
head(metag_wgs_runacc)


#library details
query <- "SELECT sample_accession, library_name, library_strategy, library_source, library_selection, library_layout, Library_construction_protocol, platform, instrument_model 
FROM sra 
WHERE (library_source = 'METAGENOMIC' AND library_strategy ='WGS')"
lib_dist <- dbGetQuery(sra_con,query)
head(lib_dist)

lib_sel <- factor(lib_dist[,5])
levels(lib_sel)
lib_lay <- factor(lib_dist[,6])
levels(lib_lay)
lib_cons <- factor(lib_dist[,7])
levels(lib_cons)

#how many metagenomic WGS studies exist? 
query <- "select study_accession from sra where (library_source = 'METAGENOMIC' AND library_strategy ='WGS')"
rs <- dbGetQuery(sra_con,query)
dim(unique.data.frame(rs))
#write.csv(unique.data.frame(rs),"C:/Users/ac133832/Documents/study_acc_mg_wgs.csv")

#how many metagenomic WGS experiments exist? -> 63416
query <- "select platform, instrument_model from experiment where (library_source = 'METAGENOMIC' AND library_strategy ='WGS')"
rs <- dbGetQuery(sra_con,query)
head(rs)
dim(rs)

#how many metagenomic WGS runs exist? -> 59617
query <- "select run_accession from sra where (library_source = 'METAGENOMIC' AND library_strategy ='WGS')"
rs <- dbGetQuery(sra_con,query)
head(rs)
dim(rs)


#platform distribution of metagenomic wgs studies? 
query <- "select distinct study.study_accession , sra.platform, sra.instrument_model 
from study
LEFT JOIN sra ON study.study_accession = sra.study_accession 
WHERE sra.library_source = 'METAGENOMIC' AND sra.library_strategy ='WGS'"
#LIMIT 10"
rs <- dbGetQuery(sra_con,query)
head(rs)
dim(rs)

rs<-rs[!(rs$instrument_model=="unspecified"),]
rs$instrument_model[rs$instrument_model=="Illumina MiSeq "] <- "Illumina MiSeq"
p<-ggplot(data=rs, aes(x=instrument_model,fill=platform)) +
  geom_bar() +
  geom_text(stat="count", aes(label=..count..), hjust=-0.1) +
  theme(axis.text.x = element_text(angle = 45, hjust = 1, size = 16), axis.text.y = element_text(hjust = 1, size = 16), legend.text = element_text(size=16)) + 
  scale_y_log10()
p + coord_flip()
write.csv(rs,"C:/Users/ac133832/Documents/study_mg_wgs_platforms.csv")

p<-ggplot() + geom_histogram(data=lib_dist, aes(x=platform, fill=library_layout), stat="count")
p

#sra accessions for all metagenomic wgs studies
query <- "select sra.run_accession, bases, sra.platform, sra.instrument_model, sra.study_accession, sra.sample_accession, sra.experiment_accession 
from sra
WHERE sra.library_source = 'METAGENOMIC' AND sra.library_strategy ='WGS'"
#LIMIT 10
rs_sra_acc <- dbGetQuery(sra_con,query)
head(rs_sra_acc)
dim(rs_sra_acc)
dim(rs_sra_acc[!duplicated(rs_sra_acc[,5]),]) #number of studies     -> 2878
dim(rs_sra_acc[!duplicated(rs_sra_acc[,6]),]) #number of samples     -> 34097
dim(rs_sra_acc[!duplicated(rs_sra_acc[,7]),]) #number of experiments -> 47765
dim(rs_sra_acc[!duplicated(rs_sra_acc[,1]),]) #number of runs        -> 59617
sum(rs_sra_acc[,2])/1000000000000             #number of bases       -> 175.6 Tb

p<-ggplot(data=rs_sra_acc, aes(y=bases)) + geom_boxplot()
p + scale_y_log10()

write.csv(rs_sra_acc,"C:/Users/ac133832/Documents/medamcan/run_acc_mg_wgs.csv", row.names = FALSE, quote=F)


acc <- getSRA(search_terms = "colon cancer",
              out_types = c("sra"), sra_con = sra_con,
              acc_only = TRUE)
g <- entityGraph(acc)
attrs <- getDefaultAttrs(list(node = list(fillcolor = "lightblue",
                                          shape = "ellipse")))
plot(g, attrs = attrs)


